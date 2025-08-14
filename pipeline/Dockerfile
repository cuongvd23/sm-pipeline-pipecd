# Install uv
FROM python:3.10 AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN curl -fsSL https://get.docker.com -o get-docker.sh &&\
  sh get-docker.sh

# Change the working directory to the `app` directory
WORKDIR /app

RUN uv venv --seed /app/venv

ENV VIRTUAL_ENV=/app/venv

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --locked --active --no-install-project

FROM python:3.10-slim

# Copy the environment
COPY --from=builder --chown=app:app /app/venv /app/venv

# Copy the docker cli
COPY --from=builder /usr/bin/docker /usr/bin/docker
COPY --from=builder /usr/libexec/docker/cli-plugins /usr/libexec/docker/cli-plugins

COPY . /app

ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app
# Run the application
CMD ["python3", "run_pipeline.py"]
