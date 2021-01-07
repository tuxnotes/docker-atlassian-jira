FROM debian:buster-backports

RUN apt-get update \
    && apt-get install -y -t buster-backports wget curl unzip yarnpkg default-jre chromium \
    && apt-get clean -y

RUN ln -s /usr/bin/yarnpkg /usr/bin/yarn

RUN wget -q https://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && rm chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver

RUN mkdir /opt/test
COPY . /opt/test
WORKDIR /opt/test

RUN yarn install
