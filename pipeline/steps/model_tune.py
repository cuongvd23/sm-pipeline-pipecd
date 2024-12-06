from sagemaker.workflow.function_step import step

from pkg.log import get_logger

logger = get_logger(__name__)


@step(display_name="model_tune")
def model_tune() -> None:
    logger.info("Start model tuning...")

    # TODO: implement me

    logger.info("Job done successfully!")
