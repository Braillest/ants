#!/bin/bash

# Copy default .env file to .env.local if it does not already exist
cp -n docker/worker/celery/.env docker/worker/celery/.env.local
