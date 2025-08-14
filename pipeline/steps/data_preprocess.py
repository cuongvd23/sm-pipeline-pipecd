import time

from sagemaker.workflow.function_step import step

from pkg.log import get_logger

logger = get_logger(__name__)


@step(display_name="data_preprocess")
def data_preprocess() -> None:
    logger.info("Start data preprocessing...")

    # TODO: implement me

    logger.warning("This is a super long running task ...")

    time.sleep(10)

    logger.info("Job done successfully!")
