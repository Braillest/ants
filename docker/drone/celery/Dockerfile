FROM python:3.13-slim-bookworm

WORKDIR /drone

# Update base image
RUN apt update
RUN apt upgrade -y
RUN apt install -y curl
RUN apt install -y autoconf
RUN apt install -y build-essential

# Create new virtual environment to install dependencies into
RUN python -m venv /env

# Install celery
RUN /env/bin/pip install --upgrade pip
RUN /env/bin/pip install celery[librabbitmq,redis]
RUN /env/bin/pip install gevent

# Install louis lib
RUN /env/bin/pip install setuptools
RUN curl -LO https://github.com/liblouis/liblouis/releases/download/v3.31.0/liblouis-3.31.0.tar.gz
RUN tar xfz liblouis-3.31.0.tar.gz
RUN cd liblouis-3.31.0 && autoconf && ./configure && make -j $(nproc) && make -j $(nproc) install && cd python && /env/bin/pip install .

# Install python deps
RUN /env/bin/pip install requests
RUN /env/bin/pip install bs4
RUN /env/bin/pip install playwright
RUN /env/bin/playwright install chromium
RUN /env/bin/playwright install-deps

# Create non-root user
RUN groupadd -r celery
RUN useradd -r -g celery celery
USER celery

ENTRYPOINT /env/bin/celery -A drone worker -P gevent --loglevel=INFO
