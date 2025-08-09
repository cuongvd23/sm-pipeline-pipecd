from sagemaker import Session
from sagemaker.config import load_sagemaker_config
from sagemaker.workflow.function_step import get_step
from sagemaker.workflow.pipeline import Pipeline

from pipeline.steps import (
    data_preprocess,
    data_validate,
    model_evaluate,
    model_train,
    model_tune,
)
from pkg.aws.sagemaker import get_session
from pkg.config.pipeline import PipelineConfig


def _get_session(config: PipelineConfig) -> Session:
    additional_sagemaker_config = load_sagemaker_config(
        additional_config_paths=["pipeline/config.yml"]
    )
    return get_session(config, additional_sagemaker_config)


def get_pipeline(config: PipelineConfig) -> Pipeline:
    sagemaker_session = _get_session(config)

    _data_preprocess = data_preprocess()
    _data_validate = data_validate()
    _model_train = model_train()
    _model_tune = model_tune()
    _model_evaluate = model_evaluate()

    get_step(_data_validate).add_depends_on([_data_preprocess])
    get_step(_model_train).add_depends_on([_data_validate])
    get_step(_model_tune).add_depends_on([_model_train])
    get_step(_model_evaluate).add_depends_on([_model_train, _model_tune])

    # Pipeline instance
    pipeline = Pipeline(
        name=f"{config.mlflow_experiment_name}-{config.name}",
        steps=[
            _data_preprocess,
            _data_validate,
            _model_train,
            _model_tune,
            _model_evaluate,
        ],
        sagemaker_session=sagemaker_session,
    )
    return pipeline
