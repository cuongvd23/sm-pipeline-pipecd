import os
from typing import Any

import boto3
import sagemaker.local.image
from sagemaker import Session
from sagemaker.local.local_session import LocalSession

from pkg.config.pipeline import PipelineConfig
from pkg.const.aws import SAGEMAKER_SERVICE_NAME
from pkg.log.logger import get_logger

logger = get_logger(__name__)


class ContainerVolume(sagemaker.local.image._Volume):
    def __init__(
        self, host_dir: str, container_dir: str | None = None, channel: str | None = None
    ) -> None:
        cwd = os.getenv("HOST_CWD")
        if cwd:
            host_dir = cwd + host_dir
        super().__init__(host_dir, container_dir, channel)


def get_session(config: PipelineConfig, sagemaker_config: dict[str, Any]) -> Session:
    boto_session = boto3.Session(region_name=config.region_name)
    if config.is_local:
        session = LocalSession(
            boto_session=boto_session,
            s3_endpoint_url=config.s3_endpoint_url,
            default_bucket=config.s3_bucket,
            default_bucket_prefix=config.s3_prefix,
        )
        sagemaker.local.image._Volume = ContainerVolume
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
