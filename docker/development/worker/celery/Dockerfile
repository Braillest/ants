FROM python:3.13-slim-bookworm

WORKDIR /worker

# Update base image
RUN apt update
RUN apt upgrade -y
RUN apt install -y curl
RUN apt install -y git
RUN apt install -y ffmpeg
RUN apt install -y autoconf
RUN apt install -y build-essential
RUN apt install -y pkg-config

# Create new virtual environment to install dependencies into
RUN python -m venv /env

# Install celery
RUN /env/bin/pip install --upgrade pip
RUN /env/bin/pip install celery[librabbitmq,redis]

# Install louis lib
RUN curl -LO https://github.com/liblouis/liblouis/releases/download/v3.38.0/liblouis-3.38.0.tar.gz && \
    tar xfz liblouis-3.38.0.tar.gz && \
    cd liblouis-3.38.0 && \
    autoconf && \
    ./configure && \
    make -j "$(nproc)" && \
    make install && \
    ldconfig && \
    cd python && \
    /env/bin/pip install --no-cache-dir setuptools && \
    /env/bin/pip install . && \
    # Cleanup to save space
    cd ../.. && \
    rm -rf liblouis-3.38.0*

# Install build123d
RUN /env/bin/pip install git+https://github.com/gumyr/build123d

# Create non-root user
RUN groupadd -r celery
RUN useradd -r -g celery celery
USER celery

ENTRYPOINT /env/bin/celery -A hard worker --loglevel=INFO
