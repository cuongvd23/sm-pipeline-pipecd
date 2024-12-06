import json
import sys

import typer
from sagemaker.local.entities import _LocalPipelineExecution

from pipeline.dag import get_pipeline
from pkg.config.pipeline import PipelineConfig
from pkg.log import get_logger

logger = get_logger(__name__)


def main(config_data: str) -> None:
    try:
        pipeline_config = PipelineConfig.load_config(config_data)
        pipeline = get_pipeline(pipeline_config)
        parsed_definition = json.loads(pipeline.definition())
        logger.info(
            "creating/updating a sagemaker pipeline",
            extra={"pipeline-definition": parsed_definition},
        )

        upsert_response = pipeline.upsert(role_arn=pipeline_config.role_arn)
        logger.info(
            "created/updated sagemaker pipeline: response received",
            extra={"response": upsert_response},
        )

        execution = pipeline.start()
        if isinstance(execution, _LocalPipelineExecution):
            logger.info("execution started with LocalPipelineExecution")
        else:
            logger.info(
                "execution started with PipelineExecutionArn",
                extra={"PipelineExecutionArn": execution.arn},
            )
    except Exception:
        logger.exception("failed to start sagemaker pipeline")
        sys.exit(1)


if __name__ == "__main__":
    typer.run(main)
