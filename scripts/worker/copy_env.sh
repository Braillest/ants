#!/bin/bash

# Copy default .env file to .env.local if it does not already exist
cp -n docker/worker/.env docker/worker/.env.local
