FROM debian:buster-backports

RUN apt-get update \
    && apt-get install -y wget unzip npm default-jre chromium \
    # NPM is fussy about being installed from backports directly, so
    # we install the base package and then upgrade
    && apt-get install -t buster-backports -y npm \
    && apt-get clean -y

RUN wget -q https://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && rm chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver

COPY dcd-builds-resources/ /dcd-builds-resources/
WORKDIR /dcd-builds-resources/jira-dc-smoke-test-suite/

RUN npm install
