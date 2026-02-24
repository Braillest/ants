#!/bin/bash

# Copy default .env file to .env.local if it does not already exist
cp -n docker/production/drone/celery/.env docker/production/drone/celery/.env.local
