#!/bin/bash

# Copy default .env file to .env.local if it does not already exist
cp -n docker/production/queen/aspnet/.env docker/production/queen/aspnet/.env.local
cp -n docker/production/queen/fastapi/.env docker/production/queen/fastapi/.env.local
cp -n docker/production/queen/flower/.env docker/production/queen/flower/.env.local
cp -n docker/production/queen/mariadb/.env docker/production/queen/mariadb/.env.local
cp -n docker/production/queen/nginx/server.conf docker/production/queen/nginx/server.conf.local
cp -n docker/production/queen/nginx/ssl.conf docker/production/queen/nginx/ssl.conf.local
cp -n docker/production/queen/phpmyadmin/.env docker/production/queen/phpmyadmin/.env.local
cp -n docker/production/queen/rabbitmq/.env docker/production/queen/rabbitmq/.env.local
cp -n docker/production/queen/redis/redis.conf docker/production/queen/redis/redis.conf.local
