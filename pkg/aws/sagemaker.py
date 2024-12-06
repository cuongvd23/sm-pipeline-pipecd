from typing import Any

import boto3
from sagemaker.workflow.pipeline import LocalSession, Session

from pkg.config.pipeline import PipelineConfig
from pkg.const.aws import SAGEMAKER_RUNTIME_SERVICE_NAME, SAGEMAKER_SERVICE_NAME


def get_session(config: PipelineConfig, sagemaker_config: dict[str, Any]) -> Session:
    boto_session = boto3.Session(region_name=config.region_name)

    if config.is_local:
        session = LocalSession(
            boto_session=boto_session,
            default_bucket=config.s3_bucket,
            default_bucket_prefix=config.s3_prefix,
            sagemaker_config=sagemaker_config,
        )
        session.config = {
            "local": {"local_code": True}
        }  # TODO: still need accessing to S3, not fully local
        return session

    sagemaker_client = boto_session.client(SAGEMAKER_SERVICE_NAME)
    runtime_client = boto_session.client(SAGEMAKER_RUNTIME_SERVICE_NAME)
    return Session(
        boto_session=boto_session,
        sagemaker_client=sagemaker_client,
        sagemaker_runtime_client=runtime_client,
        default_bucket=config.s3_bucket,
        default_bucket_prefix=config.s3_prefix,
        sagemaker_config=sagemaker_config,
    )
