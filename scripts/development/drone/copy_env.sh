#!/bin/bash

# Copy default .env file to .env.local if it does not already exist
cp -n docker/development/drone/celery/.env docker/development/drone/celery/.env.local
