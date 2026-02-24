FROM redis:8.4.0-alpine

COPY docker/production/queen/redis/redis.conf.local /usr/local/etc/redis/redis.conf

ENTRYPOINT redis-server /usr/local/etc/redis/redis.conf
