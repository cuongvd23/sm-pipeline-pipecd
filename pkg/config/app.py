from .base import BaseConfig


class AppConfig(BaseConfig):
    mlflow_registered_model_uri: str
