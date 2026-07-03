# Networking

For running all services locally on the same device for testing purposes, be sure to use the following environment variables:

- CELERY_BROKER_URL=amqp://pawn:**@ants_development_queen_rabbitmq:5672//
- CELERY_RESULT_BACKEND=redis://ants_development_queen_redis:6379/0
