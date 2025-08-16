from __future__ import annotations

import base64
from typing import Self

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from pydantic.alias_generators import to_camel

from pkg.log import get_logger

logger = get_logger(__name__)


class BaseConfig(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    region_name: str
    time_zone: str

    mlflow_tracking_server_uri: str = Field(
        serialization_alias="mlflow_tracking_server_arn"
    )

    @classmethod
    def load_config(cls, config_base64: str) -> Self:
        try:
            config_yaml = base64.b64decode(config_base64).decode("utf-8")
            config_dict = yaml.safe_load(config_yaml)
            config = cls.model_validate(config_dict)
        except ValidationError:
            logger.exception("Configuration validation error")
            print(config_yaml)
            raise
        except:
            logger.exception("Load configuration error")
            raise

        return config
