FROM nginx:bookworm

RUN apt update
RUN apt upgrade -y

RUN mkdir -p /etc/nginx/ssl

# Copy config
COPY docker/queen/nginx/ssl.conf.local /tmp/ssl.conf
COPY docker/queen/nginx/server.conf.local /etc/nginx/conf.d/server.conf

# Generate the key and cert (valid for 1 year)
RUN openssl req -x509 -nodes -days 365 -newkey rsa:4096 -keyout /etc/nginx/ssl/queen.key -out /etc/nginx/ssl/queen.crt -config /tmp/ssl.conf
