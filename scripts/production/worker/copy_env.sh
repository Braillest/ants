#!/bin/bash

# Copy default .env file to .env.local if it does not already exist
cp -n docker/production/worker/celery/.env docker/production/worker/celery/.env.local
