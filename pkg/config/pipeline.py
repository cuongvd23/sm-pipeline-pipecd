from pydantic import Field

from .base import BaseConfig


class PipelineConfig(BaseConfig):
    name: str
    role_arn: str
    s3_prefix: str
    s3_bucket: str
    s3_endpoint_url: str | None

    mlflow_experiment_name: str

    is_local: bool = Field(default=False)
