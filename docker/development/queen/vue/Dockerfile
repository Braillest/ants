FROM node:25-bookworm-slim

WORKDIR /vue

COPY docker/development/queen/vue/startup.sh /tmp/startup.sh

ENTRYPOINT ["/tmp/startup.sh"]
