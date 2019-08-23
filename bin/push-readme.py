import logging
import os

import requests


logging.basicConfig(level=logging.INFO)


DOCKER_REPO = os.environ.get('DOCKER_REPO')
DOCKER_USERNAME = os.environ.get('DOCKER_USERNAME')
DOCKER_PASSWORD = os.environ.get('DOCKER_PASSWORD')
DOCKER_TOKEN = os.environ.get('DOCKER_TOKEN')
README_FILE = os.environ.get('README_FILE') or 'README.md'


if DOCKER_TOKEN is None:
    logging.info('Generating Docker Hub JWT')
    data = {'username': DOCKER_USERNAME, 'password': DOCKER_PASSWORD}
    r = requests.post('https://hub.docker.com/v2/users/login/', json=data)
    token = r.json().get('token')
    DOCKER_TOKEN = os.environ.setdefault('DOCKER_TOKEN', token)

with open(README_FILE) as f:
    full_description = f.read()

headers = {'Authorization': f'JWT {DOCKER_TOKEN}'}

data = {
    'registry': 'registry-1.docker.io',
    'full_description': full_description
}

logging.info(f'Patching Docker Hub description for {DOCKER_REPO}')
r = requests.patch(f'https://cloud.docker.com/v2/repositories/{DOCKER_REPO}/',
                   headers=headers, json=data)

if r.status_code == requests.codes.ok:
    logging.info(f'Successfully pushed {README_FILE} for {DOCKER_REPO}')
else:
    logging.info(f'Unable to push {README_FILE} for {DOCKER_REPO}, response code: {r.status_code}')