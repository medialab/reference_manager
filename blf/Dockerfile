FROM nginx:alpine

ENV PUBLIC_URL http://localhost:3000
ENV API_HOST api
ENV API_PORT 8080

COPY . /blf

RUN rm /etc/nginx/conf.d/default.conf

COPY ./docker-nginx.conf /etc/nginx/conf.d/docker.template

CMD /bin/sh /blf/docker-cmd.sh
