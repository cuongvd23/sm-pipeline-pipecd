from sagemaker.workflow.function_step import step

from pkg.log import get_logger

logger = get_logger(__name__)


@step(display_name="model_train")
def model_train() -> None:
    logger.info("Start model training...")

    # TODO: implement me

    logger.info("Job done successfully!")
