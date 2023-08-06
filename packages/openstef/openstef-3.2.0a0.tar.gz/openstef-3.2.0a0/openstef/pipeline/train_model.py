# SPDX-FileCopyrightText: 2017-2022 Contributors to the OpenSTEF project <korte.termijn.prognoses@alliander.com> # noqa E501>
#
# SPDX-License-Identifier: MPL-2.0
import logging
from pathlib import Path
from typing import List, Tuple, Union

import pandas as pd
import structlog

from openstef.data_classes.model_specifications import ModelSpecificationDataClass
from openstef.data_classes.prediction_job import PredictionJobDataClass
from openstef.exceptions import (
    InputDataInsufficientError,
    InputDataWrongColumnOrderError,
    OldModelHigherScoreError,
)
from openstef.feature_engineering.feature_applicator import TrainFeatureApplicator
from openstef.metrics.reporter import Report, Reporter
from openstef.model.model_creator import ModelCreator
from openstef.model.regressors.regressor import OpenstfRegressor
from openstef.model.serializer import MLflowSerializer
from openstef.model.standard_deviation_generator import StandardDeviationGenerator
from openstef.model_selection.model_selection import split_data_train_validation_test
from openstef.validation import validation

DEFAULT_TRAIN_HORIZONS: List[float] = [0.25, 47.0]
MAXIMUM_MODEL_AGE: int = 7

DEFAULT_EARLY_STOPPING_ROUNDS: int = 10
PENALTY_FACTOR_OLD_MODEL: float = 1.2


def train_model_pipeline(
    pj: PredictionJobDataClass,
    input_data: pd.DataFrame,
    check_old_model_age: bool,
    mlflow_tracking_uri: str,
    trained_models_folder: Union[str, Path],
) -> Report:
    """Middle level pipeline that takes care of all persistent storage dependencies

    Expected prediction jobs keys: "id", "model", "hyper_params", "feature_names"

    Args:
        pj (PredictionJobDataClass): Prediction job
        input_data (pd.DataFrame): Raw training input data
        check_old_model_age (bool): Check if training should be skipped because the model is too young
        mlflow_tracking_uri (str): Tracking URI for MLFlow
        trained_models_folder (Path): Path where trained models are stored

    Returns:
        report (Report): The report containing train/val/test datasets and corresponding forecasts if requested
    """
    # Initialize logger and serializer
    logger = structlog.get_logger(__name__)
    serializer = MLflowSerializer(
        mlflow_tracking_uri=mlflow_tracking_uri, artifact_root=trained_models_folder
    )

    # Get old model and age
    try:
        old_model, model_specs = serializer.load_model(experiment_name=pj["id"])
        old_model_age = old_model.age  # Age attribute is openstef specific
    except (AttributeError, FileNotFoundError, LookupError):
        old_model = None
        old_model_age = float("inf")
        if pj["default_modelspecs"] is not None:
            model_specs = pj["default_modelspecs"]
            if model_specs.id != pj.id:
                raise RuntimeError(
                    "The id of the prediction job and its default model_specs do not"
                    " match."
                )
        else:
            # create basic model_specs
            model_specs = ModelSpecificationDataClass(id=pj["id"])
        logger.warning("No old model found, training new model", pid=pj["id"])

    # Check old model age and continue yes/no
    if (old_model_age < MAXIMUM_MODEL_AGE) and check_old_model_age:
        logger.warning(
            f"Old model is younger than {MAXIMUM_MODEL_AGE} days, skip training"
        )
        return

    # Train model with core pipeline
    try:
        model, report, model_specs_updated = train_model_pipeline_core(
            pj, model_specs, input_data, old_model, horizons=pj.train_horizons_minutes
        )
    except OldModelHigherScoreError as OMHSE:
        logger.error("Old model is better than new model", pid=pj["id"], exc_info=OMHSE)
        return

    except InputDataInsufficientError as IDIE:
        logger.error(
            "Input data is insufficient after validation and cleaning",
            pid=pj["id"],
            exc_info=IDIE,
        )
        raise InputDataInsufficientError(IDIE)

    except InputDataWrongColumnOrderError as IDWCOE:
        logger.error(
            "Wrong column order, 'load' column should be first and 'horizon' column"
            " last.",
            pid=pj["id"],
            exc_info=IDWCOE,
        )
        raise InputDataWrongColumnOrderError(IDWCOE)

    # Save model and report. Report is always saved to MLFlow and optionally to disk
    serializer.save_model(
        model=model,
        experiment_name=str(pj["id"]),
        model_type=pj["model"],
        model_specs=model_specs_updated,
        report=report,
    )
    if trained_models_folder:
        Reporter.write_report_to_disk(report=report, location=trained_models_folder)

    # Clean up older models
    serializer.remove_old_models(experiment_name=str(pj["id"]))
    return report


def train_model_pipeline_core(
    pj: PredictionJobDataClass,
    model_specs: ModelSpecificationDataClass,
    input_data: pd.DataFrame,
    old_model: OpenstfRegressor = None,
    horizons: Union[List[float], str] = None,
) -> Tuple[OpenstfRegressor, Report, ModelSpecificationDataClass]:
    """Train model core pipeline.
    Trains a new model given a prediction job, input data and compares it to an old model.
    This pipeline has no database or persistent storage dependencies.

    Args:
        pj (PredictionJobDataClass): Prediction job
        model_specs (ModelSpecificationDataClass): Dataclass containing model specifications
        input_data (pd.DataFrame): Input data
        old_model (OpenstfRegressor, optional): Old model to compare to. Defaults to None.
        horizons (List[float]): horizons to train on in hours.

    Raises:
        InputDataInsufficientError: when input data is insufficient.
        InputDataWrongColumnOrderError: when input data has a invalid column order.
        OldModelHigherScoreError: When old model is better than new model.

    Returns:
        Tuple[OpenstfRegressor, Report, ModelSpecificationDataClass]: Trained model and report (with figures)
    """

    if horizons is None:
        if pj.train_horizons_minutes is None:
            horizons = DEFAULT_TRAIN_HORIZONS
        else:
            horizons = pj.train_horizons_minutes

    logger = structlog.get_logger(__name__)

    # Call common pipeline
    model, report, train_data, validation_data, test_data = train_pipeline_common(
        pj, model_specs, input_data, horizons
    )
    model_specs.feature_names = list(train_data.columns)

    # Check if new model is better than old model
    if old_model:
        combined = train_data.append(validation_data).reset_index(drop=True)
        x_data, y_data = (
            combined.iloc[:, 1:-1],
            combined.iloc[:, 0],
        )

        # Score method always returns R^2
        score_new_model = model.score(x_data, y_data)

        # Try to compare new model to old model.
        # If this does not success, for example since the feature names of the
        # old model differ from the new model, the new model is considered better
        try:
            score_old_model = old_model.score(x_data, y_data)

            # Check if R^2 is better for old model
            if score_old_model > score_new_model * PENALTY_FACTOR_OLD_MODEL:
                raise OldModelHigherScoreError(
                    f"Old model is better than new model for {pj['id']}."
                )

            logger.info(
                "New model is better than old model, continuing with training procces"
            )
        except ValueError as e:
            logger.info("Could not compare to old model", pid=pj["id"], exc_info=e)

    return model, report, model_specs


def train_pipeline_common(
    pj: PredictionJobDataClass,
    model_specs: ModelSpecificationDataClass,
    input_data: pd.DataFrame,
    horizons: Union[List[float], str],
    test_fraction: float = 0.0,
    backtest: bool = False,
    test_data_predefined: pd.DataFrame = pd.DataFrame(),
) -> Tuple[OpenstfRegressor, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Common pipeline shared with operational training and backtest training

    Args:
        pj (PredictionJobDataClass): Prediction job
        model_specs (ModelSpecificationDataClass): Dataclass containing model specifications
        input_data (pd.DataFrame): Input data
        horizons (List[float]): horizons to train on in hours.
        test_fraction (float): fraction of data to use for testing
        backtest (bool): boolean if we need to do a backtest
        test_data_predefined (pd.DataFrame): Predefined test data frame to be used in the pipeline
            (empty data frame by default)

    Returns:
        Tuple[RegressorMixin, Report, pd.DataFrame, pd.DataFrame, pd.DataFrame]: Trained model, report
         train_data, validation_data and test_data

    Raises:
        InputDataInsufficientError: when input data is insufficient.
        InputDataWrongColumnOrderError: when input data has a invalid column order.

    """
    if input_data.empty:
        raise InputDataInsufficientError("Input dataframe is empty")
    elif "load" not in input_data.columns:
        raise InputDataWrongColumnOrderError(
            "Missing the load column in the input dataframe"
        )

    if isinstance(horizons, str):
        if not (horizons in set(input_data.columns)):
            raise ValueError(
                f"The horizon parameter specifies a column name ({horizons}) missing in"
                " the input data."
            )
        else:
            # sort data to avoid same date repeated multiple time
            input_data = input_data.sort_values(horizons)
    # Validate and clean data
    validated_data = validation.drop_target_na(
        validation.validate(pj["id"], input_data, pj["flatliner_treshold"])
    )
    # Check if sufficient data is left after cleaning
    if not validation.is_data_sufficient(
        validated_data, pj["completeness_treshold"], pj["minimal_table_length"]
    ):
        raise InputDataInsufficientError(
            "Input data is insufficient, after validation and cleaning"
        )

    if pj["model"] == "proloaf":
        stratification_min_max = False
        # proloaf is only able to train with one horizon
        horizons = [horizons[0]]
    else:
        stratification_min_max = True

    data_with_features = TrainFeatureApplicator(
        horizons=horizons,
        feature_names=model_specs.feature_names,
        feature_modules=model_specs.feature_modules,
    ).add_features(validated_data, pj=pj)

    # if test_data is predefined, apply the pipeline only on the remaining data
    if not test_data_predefined.empty:
        test_data_predefined = data_with_features[
            data_with_features.index.isin(test_data_predefined.index)
        ].sort_index()
        data_with_features = data_with_features[
            ~data_with_features.index.isin(test_data_predefined.index)
        ].sort_index()

    # Split data
    (train_data, validation_data, test_data,) = split_data_train_validation_test(
        data_with_features,
        test_fraction=test_fraction,
        stratification_min_max=stratification_min_max,
        back_test=backtest,
    )

    # if test_data is predefined, use this over the returned test_data of split function
    if not test_data_predefined.empty:
        test_data = test_data_predefined

    # Test if first column is "load" and last column is "horizon"
    if train_data.columns[0] != "load" or train_data.columns[-1] != "horizon":
        raise InputDataWrongColumnOrderError(
            f"Wrong column order for {pj['id']} "
            "'load' column should be first and 'horizon' column last."
        )

    # Create relevant model
    model = ModelCreator.create_model(
        pj["model"],
        quantiles=pj["quantiles"],
    )

    # split x and y data
    train_x, train_y = train_data.iloc[:, 1:-1], train_data.iloc[:, 0]
    validation_x, validation_y = (
        validation_data.iloc[:, 1:-1],
        validation_data.iloc[:, 0],
    )

    # Configure evals for early stopping
    eval_set = [(train_x, train_y), (validation_x, validation_y)]

    # Set relevant hyperparameters
    # define protected hyperparams which are derived from prediction_job
    protected_hyperparams = ["quantiles"]
    valid_hyper_parameters = {
        key: value
        for key, value in model_specs.hyper_params.items()
        if key in model.get_params().keys() and key not in protected_hyperparams
    }

    model.set_params(**valid_hyper_parameters)
    model.fit(
        train_x,
        train_y,
        eval_set=eval_set,
        early_stopping_rounds=DEFAULT_EARLY_STOPPING_ROUNDS,
        verbose=False,
    )
    # Gets the feature importance df or None if we don't have feature importance
    model.feature_importance_dataframe = model.set_feature_importance()

    logging.info("Fitted a new model, not yet stored")

    # Do confidence interval determination
    model = StandardDeviationGenerator(
        validation_data
    ).generate_standard_deviation_data(model)

    if pj.save_train_forecasts:
        train_data["forecast"] = model.predict(train_data).values
        validation_data["forecast"] = model.predict(validation_data).values
        test_data["forecast"] = model.predict(test_data).values

    # Report about the training process
    reporter = Reporter(train_data, validation_data, test_data)
    report = reporter.generate_report(model)

    return model, report, train_data, validation_data, test_data
