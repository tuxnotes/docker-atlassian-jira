FROM node:14.16.0-buster

RUN apt-get update \
    && apt-get install -y wget curl unzip \
    && apt-get clean -y

RUN mkdir /opt/test
COPY . /opt/test
WORKDIR /opt/test

RUN yarn install
