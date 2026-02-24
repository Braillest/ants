FROM python:3.13-slim-bookworm

WORKDIR /flower

# Update base image
RUN apt update
RUN apt upgrade -y

# Create new virtual environment to install dependencies into
RUN python -m venv /env

# Install pip packages and deps
RUN /env/bin/pip install --upgrade pip
RUN /env/bin/pip install celery[librabbitmq,redis]
RUN /env/bin/pip install flower

# Create non-root user
RUN groupadd -r celery
RUN useradd -r -g celery celery
USER celery

ENTRYPOINT /env/bin/celery flower --broker=$CELERY_BROKER_URL --loglevel=INFO
