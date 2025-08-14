import os
from typing import Any

import boto3
import sagemaker.local.image
import yaml
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
            logger.warning("Patching container volume")
            host_dir = cwd + host_dir
        super().__init__(host_dir, container_dir, channel)  # type: ignore[no-untyped-call]


class SageMakerContainer(sagemaker.local.image._SageMakerContainer):
    def _generate_compose_file(
        self,
        command: str,
        additional_volumes: list[str] | None = None,
        additional_env_vars: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        content: dict[str, Any] = super()._generate_compose_file(
            command, additional_volumes, additional_env_vars
        )  # type: ignore[no-untyped-call]

        if content.get("networks", {}).get("sagemaker-local"):
            logger.warning("Patching docker-compose.yaml")

            if content.get("version"):
                del content["version"]

            content["networks"]["sagemaker-local"]["external"] = True

            docker_compose_path = os.path.join(
                self.container_root or "",
                sagemaker.local.image.DOCKER_COMPOSE_FILENAME,
            )

            yaml_content = yaml.dump(content, default_flow_style=False)
            with open(docker_compose_path, "w") as f:
                f.write(yaml_content)

        return content


def get_session(config: PipelineConfig, sagemaker_config: dict[str, Any]) -> Session:
    boto_session = boto3.Session(region_name=config.region_name)
    if config.is_local:
        session = LocalSession(
            boto_session=boto_session,
            s3_endpoint_url=config.s3_endpoint_url,
            default_bucket=config.s3_bucket,
            default_bucket_prefix=config.s3_prefix,
        )
        sagemaker.local.entities._SageMakerContainer = SageMakerContainer  # type: ignore[misc]
        sagemaker.local.image._SageMakerContainer = SageMakerContainer  # type: ignore[misc]
        sagemaker.local.local_session._SageMakerContainer = SageMakerContainer  # type: ignore[misc]
        sagemaker.local.image._Volume = ContainerVolume  # type: ignore[misc]
        sagemaker.local.image.S3_ENDPOINT_URL_ENV_NAME = "AWS_ENDPOINT_URL_S3"
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
