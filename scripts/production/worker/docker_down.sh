#!/bin/bash

docker compose -f production-worker-docker-compose.yml down --rmi all
