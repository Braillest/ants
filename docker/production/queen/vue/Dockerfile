# build stage
FROM node:lts-alpine AS build-stage
WORKDIR /vue
COPY ./src/vue/package.json .
COPY ./src/vue/package-lock.json .
RUN npm install
COPY ./src/vue/ .
RUN npm run build

# production stage
FROM nginx:stable-alpine AS production-stage
RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/production/queen/vue/nginx.conf.local /etc/nginx/conf.d/nginx.conf
COPY --from=build-stage /vue/dist /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]
