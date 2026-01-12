#!/bin/bash

# Copy default .env file to .env.local if it does not already exist
cp -n docker/queen/aspnet/.env docker/queen/aspnet/.env.local
cp -n docker/queen/fastapi/.env docker/queen/fastapi/.env.local
cp -n docker/queen/flower/.env docker/queen/flower/.env.local
cp -n docker/queen/mariadb/.env docker/queen/mariadb/.env.local
cp -n docker/queen/nginx/server.conf docker/queen/nginx/server.conf.local
cp -n docker/queen/nginx/ssl.conf docker/queen/nginx/ssl.conf.local
cp -n docker/queen/phpmyadmin/.env docker/queen/phpmyadmin/.env.local
cp -n docker/queen/rabbitmq/.env docker/queen/rabbitmq/.env.local
cp -n docker/queen/redis/redis.conf docker/queen/redis/redis.conf.local
