FROM python:3.10.16 AS build
RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip

FROM build AS build-venv

ENV PATH="/venv/bin:$PATH"

ARG POETRY_VERSION="1.8.3"
RUN pip install --disable-pip-version-check poetry==${POETRY_VERSION}

COPY poetry.lock /poetry.lock
COPY pyproject.toml /pyproject.toml

RUN . /venv/bin/activate && poetry install --only main --sync

FROM python:3.10.16-slim

COPY --from=build-venv /venv /venv
COPY . /app

WORKDIR /app
CMD ["/venv/bin/python3", "run_pipeline.py"]
