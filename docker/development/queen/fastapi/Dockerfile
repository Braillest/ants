FROM ubuntu:jammy

WORKDIR /fastapi

# Get latest apt updates and upgrades
RUN apt update
RUN apt upgrade -y

# Install python3
RUN apt install -y python3-full

# Create new virtual environment to install dependencies into
RUN python3 -m venv /env

# Install pip packages and deps
RUN /env/bin/pip install --upgrade pip
RUN /env/bin/pip install celery[librabbitmq,redis]
RUN /env/bin/pip install requests
RUN /env/bin/pip install fastapi[standard]
RUN /env/bin/pip install starlette
RUN /env/bin/pip install uvicorn
RUN /env/bin/pip install pydantic

# ENTRYPOINT sleep infinity
ENTRYPOINT /env/bin/fastapi dev task-server.py --host 0.0.0.0
