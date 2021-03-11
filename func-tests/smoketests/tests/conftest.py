
from dataclasses import dataclass
import logging
import os
import pytest
import requests
from requests.auth import HTTPBasicAuth
import time


@dataclass
class Context:
    base_url: str
    admin_user: str
    admin_pwd: str
    user_name: str
    user_pwd: str
    indexing_timeout: int = 30 * 1000

    def __post_init__(self):
        self.admin_auth = HTTPBasicAuth(self.admin_user, self.admin_pwd)
        self.user_auth = HTTPBasicAuth(self.user_name, self.user_pwd)


@pytest.fixture(scope='session')
def ctx():
    return Context(
        base_url=os.environ.get('JIRA_BASEURL', "http://jira:8080/jira"),
        admin_user=os.environ.get('JIRA_ADMIN', 'admin'),
        admin_pwd=os.environ.get('JIRA_ADMIN_PWD', 'admin'),
        user_name=os.environ.get('JIRA_USER', 'admin'),
        user_pwd=os.environ.get('JIRA_USER_PWD', 'admin')
    )


@pytest.fixture(scope='session', autouse=True)
def reindex_before_tests(ctx):
    reindex = ctx.base_url + "/rest/api/2/reindex"
    progress = reindex + "/progress"

    logging.info("Starting reindexing...")
    resp = requests.post(reindex, auth=ctx.admin_auth)
    assert resp.status_code == 202

    delay_ms = 500
    for _ in range(0, int(ctx.indexing_timeout / delay_ms)):
        resp = requests.get(progress, auth=ctx.admin_auth)
        assert resp.status_code == 200
        logging.info("JSON: "+str(resp.json()))
        if resp.json()['currentProgress'] >= 100:
            logging.info("Indexing complete")
            return

        time.sleep(delay_ms/1000)

    logging.info("Indexing timed-out")
    pytest.fail("Indexing timed-out")
