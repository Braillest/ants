# Networking

For running all services locally on the same device for testing purposes, be sure to use the following environment variables:

- CELERY_BROKER_URL=amqp://pawn:**@host.docker.internal:5672//
- CELERY_RESULT_BACKEND=redis://host.docker.internal:6379/0
