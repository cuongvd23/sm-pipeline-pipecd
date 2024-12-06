from sagemaker.workflow.function_step import step

from pkg.log import get_logger

logger = get_logger(__name__)


@step(display_name="data_validate")
def data_validate() -> None:
    logger.info("Start data validating...")

    # TODO: implement me

    logger.info("Job done successfully!")
