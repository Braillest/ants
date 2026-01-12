#!/bin/bash

# Copy default .env file to .env.local if it does not already exist
cp -n docker/drone/.env docker/drone/.env.local
