import time

from sagemaker.workflow.function_step import step


@step(display_name="model_train")
def model_train() -> None:
    from pkg.log import get_logger

    logger = get_logger(__name__)

    logger.info("Start model training...")

    # TODO: implement me
    logger.warning("This is a super long running task ...")

    time.sleep(10)

    logger.info("Job done successfully!")
