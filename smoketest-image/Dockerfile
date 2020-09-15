FROM debian:buster

RUN echo "deb http://deb.debian.org/debian buster-backports main" > /etc/apt/sources.list.d/buster-backports.list \
    && apt-get update \
    && apt-get install -t buster-backports -y wget unzip npm \
    && apt-get clean -y

RUN wget -N https://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    rm chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver

COPY dcd-builds-resources/ /dcd-builds-resources/
WORKDIR /dcd-builds-resources/jira-dc-smoke-test-suite/

RUN npm install
