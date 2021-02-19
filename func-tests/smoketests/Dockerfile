FROM debian:buster-backports

RUN apt-get update \
    && apt-get install -y -t buster-backports wget curl unzip yarnpkg \
    && apt-get clean -y

RUN ln -s /usr/bin/yarnpkg /usr/bin/yarn

RUN mkdir /opt/test
COPY . /opt/test
WORKDIR /opt/test

RUN yarn install
