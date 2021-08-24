FROM python:3.9.5

RUN apt-get update \
    && apt-get install -y pipenv \
    && apt-get clean -y

RUN mkdir /opt/test
COPY . /opt/test
WORKDIR /opt/test

RUN pipenv install --dev
