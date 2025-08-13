# ruff: noqa: E402

from pkg.log import get_logger

_ = get_logger("sagemaker")
_ = get_logger("sagemaker.config")
_ = get_logger("sagemaker.remote_function")


import typer

from main import main

if __name__ == "__main__":
    typer.run(main)
