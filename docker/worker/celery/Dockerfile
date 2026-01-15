FROM python:3.13-slim-bookworm

WORKDIR /worker

# Update base image
RUN apt update
RUN apt upgrade -y
RUN apt install -y git
RUN apt install -y ffmpeg

# Create new virtual environment to install dependencies into
RUN python -m venv /env

# Install celery
RUN /env/bin/pip install --upgrade pip
RUN /env/bin/pip install celery[librabbitmq,redis]

# Install build123d
RUN /env/bin/pip install git+https://github.com/gumyr/build123d

# Create non-root user
RUN groupadd -r celery
RUN useradd -r -g celery celery
USER celery

ENTRYPOINT /env/bin/celery -A worker worker --loglevel=INFO
