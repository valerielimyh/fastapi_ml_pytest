# pull official base image
FROM tiangolo/uvicorn-gunicorn:python3.8

LABEL maintainer='valerielim <valerieeelimyh@gmail.com>'

# set work directory
WORKDIR /fastapi_ml_pytest

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# copy requirements file
COPY ./pyproject.toml ./poetry.lock /fastapi_ml_pytest/

RUN poetry install --no-root --no-dev

# copy project
COPY . .