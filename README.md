# SageMaker Pipeline with PipeCD

A comprehensive MLOps solution showcasing AWS SageMaker pipeline orchestration with CI/CD automation using PipeCD.

## Overview

This project demonstrates a machine learning pipeline built on AWS SageMaker with automated deployment through PipeCD.
This project supports testing and validating AWS SageMaker pipeline on the local machine with Docker Engine installed.

## Features

- **📊 ML Pipeline**: 5-step SageMaker pipeline with data preprocessing, validation, training, tuning, and evaluation
- **🚀 CI/CD Integration**: Automated deployment using PipeCD with ECS
- **🐳 Local Development**: Docker Compose setup with MinIO for S3-compatible local testing
- **🔍 Code Quality**: Integrated linting, formatting, and type checking with Ruff and MyPy
- **📝 Structured Logging**: Comprehensive logging with colorlog for better observability
- **⚙️ Configuration Management**: Pydantic-based configuration with Base64 encoding

## Quick Start

### Prerequisites

- Python 3.13
- UV package manager (Reccommend)
- Docker and Docker Compose

### Installation

```bash
# Install dependencies
uv sync

# For development with type checking
uv sync --group typing
```

### Local Mode

1. Set up environment variables:

```bash
export HOST_CWD=$(pwd)
export CONFIG_DATA=<base64_encoded_config> # eg. macos: cat pipecd/pipeline-config.yaml | base64

cp .env.example .env
vi .env
```

2. Run with Docker Compose:

- MinIO server on ports 9000/9001 for S3-compatible storage

```bash
docker compose up -d minio
```

- SageMaker pipeline container with local execution

```bash
docker compose up --build pipeline
```

## Pipeline Architecture

The ML pipeline consists of five sequential steps:

```
data_preprocess → data_validate → model_train → model_tune
                                                    ↓
                                              model_evaluate
```

1. **Data Preprocessing**: Initial data cleaning and preparation
2. **Data Validation**: Data quality checks and validation
3. **Model Training**: Train the machine learning model
4. **Model Tuning**: Hyperparameter optimization
5. **Model Evaluation**: Performance assessment and metrics generation

## Development

### Code Quality

```bash
# Setup environment
uv sync --locked --all-groups

# Linting
uv run ruff check
uv run ruff check --fix  # Auto-fix issues

# Code formatting
uv run ruff format

# Type checking
uv run mypy .
```

### Project Structure

```
.
├── pipeline/                 # SageMaker pipeline definition
│   ├── steps/               # Individual pipeline steps
│   ├── dag.py              # Pipeline orchestration
│   └── config.yml          # SageMaker configuration
├── pkg/                     # Shared packages
│   ├── aws/                # AWS integrations
│   ├── config/             # Configuration management
│   ├── const/              # Constants
│   └── log/                # Logging utilities
├── pipecd/                 # PipeCD deployment configs
├── main.py                 # Main pipeline logic
├── run_pipeline.py         # Entry point with logging
└── docker-compose.yaml     # Local development stack
```

## Deployment

### PipeCD Integration

The project uses PipeCD for automated ECS deployment with:

- **Application Configuration**: `pipecd/app.pipecd.yaml`
- **Task Definition**: `pipecd/taskdef.yaml`
- **Event Watchers**: Automated image updates on new builds

### Configuration

Pipeline configuration uses Pydantic models with Base64 encoding:

```python
class PipelineConfig:
    name: str
    role_arn: str
    s3_bucket: str
    s3_prefix: str
    s3_endpoint_url: str | None
    mlflow_experiment_name: str
    is_local: bool
```
