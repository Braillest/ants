#!/bin/bash

# Copy default .env file to .env.local if it does not already exist
cp -n docker/development/worker/celery/.env docker/development/worker/celery/.env.local
