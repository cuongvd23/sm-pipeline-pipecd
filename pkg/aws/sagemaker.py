from typing import Any

import boto3
from sagemaker import Session
from sagemaker.local.local_session import LocalSession

from pkg.config.pipeline import PipelineConfig
from pkg.const.aws import SAGEMAKER_SERVICE_NAME


def get_session(config: PipelineConfig, sagemaker_config: dict[str, Any]) -> Session:
    boto_session = boto3.Session(region_name=config.region_name)
    if config.is_local:
        session = LocalSession(
            boto_session=boto_session,
            s3_endpoint_url=config.s3_endpoint_url,
            default_bucket=config.s3_bucket,
            default_bucket_prefix=config.s3_prefix,
        )
        session.sagemaker_config = sagemaker_config
        session.config = {"local": {"local_code": True}}
        return session

    sagemaker_client = boto_session.client(SAGEMAKER_SERVICE_NAME)
    return Session(
        boto_session=boto_session,
        sagemaker_client=sagemaker_client,
        default_bucket=config.s3_bucket,
        default_bucket_prefix=config.s3_prefix,
        sagemaker_config=sagemaker_config,
    )
