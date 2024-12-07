import os
from typing import Any

import boto3
import botocore
import sagemaker.local.image as sm_local_image
import sagemaker.utils as sm_utils
from sagemaker import Session
from sagemaker.workflow.pipeline_context import LocalPipelineSession, PipelineSession

from pkg.config.pipeline import PipelineConfig
from pkg.const.aws import SAGEMAKER_SERVICE_NAME


def get_session(config: PipelineConfig, sagemaker_config: dict[str, Any]) -> Session:
    boto_session = boto3.Session(region_name=config.region_name)
    if config.is_local:
        session = LocalPipelineSession(
            boto_session=boto_session,
            s3_endpoint_url=config.s3_endpoint_url,
            default_bucket=config.s3_bucket,
            default_bucket_prefix=config.s3_prefix,
        )
        session.sagemaker_config = sagemaker_config
        session.config = {"local": {"local_code": True}}
        __inject_s3()  # inject bad S3 of SDK # TODO: remove when SDK fixed
        return session

    sagemaker_client = boto_session.client(SAGEMAKER_SERVICE_NAME)
    return PipelineSession(
        boto_session=boto_session,
        sagemaker_client=sagemaker_client,
        default_bucket=config.s3_bucket,
        default_bucket_prefix=config.s3_prefix,
        sagemaker_config=sagemaker_config,
    )


def __inject_s3() -> None:
    sm_utils.download_folder = __download_folder
    sm_local_image.S3_ENDPOINT_URL_ENV_NAME = "AWS_ENDPOINT_URL_S3"


def __download_folder(bucket_name, prefix, target, sagemaker_session) -> None:
    """Download a folder from S3 to a local path

    Args:
        bucket_name (str): S3 bucket name
        prefix (str): S3 prefix within the bucket that will be downloaded. Can
            be a single file.
        target (str): destination path where the downloaded items will be placed
        sagemaker_session (sagemaker.session.Session): a sagemaker session to
            interact with S3.
    """
    s3 = sagemaker_session.s3_resource

    prefix = prefix.lstrip("/")

    # Try to download the prefix as an object first, in case it is a file and not a 'directory'.
    # Do this first, in case the object has broader permissions than the bucket.
    if not prefix.endswith("/"):
        try:
            file_destination = os.path.join(target, os.path.basename(prefix))
            s3.Object(bucket_name, prefix).download_file(file_destination)
            return
        except botocore.exceptions.ClientError as e:
            err_info = e.response["Error"]
            if err_info["Code"] == "404" and err_info["Message"] == "Not Found":
                # S3 also throws this error if the object is a folder,
                # so assume that is the case here, and then raise for an actual 404 later.
                pass
            else:
                raise

    sm_utils._download_files_under_prefix(bucket_name, prefix, target, s3)
