#!/bin/bash

# Copy default .env file to .env.local if it does not already exist
cp -n docker/development/queen/aspnet/.env docker/development/queen/aspnet/.env.local
cp -n docker/development/queen/fastapi/.env docker/development/queen/fastapi/.env.local
cp -n docker/development/queen/flower/.env docker/development/queen/flower/.env.local
cp -n docker/development/queen/mariadb/.env docker/development/queen/mariadb/.env.local
cp -n docker/development/queen/nginx/server.conf docker/development/queen/nginx/server.conf.local
cp -n docker/development/queen/nginx/ssl.conf docker/development/queen/nginx/ssl.conf.local
cp -n docker/development/queen/phpmyadmin/.env docker/development/queen/phpmyadmin/.env.local
cp -n docker/development/queen/rabbitmq/.env docker/development/queen/rabbitmq/.env.local
cp -n docker/development/queen/redis/redis.conf docker/development/queen/redis/redis.conf.local
