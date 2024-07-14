FROM alpine
RUN apk add --no-cache python3
COPY assets assets
RUN tar -xf /assets/mysql.tar.xz --directory /usr/lib/python3.12/
EXPOSE 7779