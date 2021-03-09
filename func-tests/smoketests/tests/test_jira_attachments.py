
from datetime import datetime
from functools import reduce
import json
import logging
import pytest
import requests
import tempfile

NOCHECK = {"X-Atlassian-Token": "no-check"}

@pytest.fixture(scope='session')
def attachment_file(ctx):
    _fd, fname =  tempfile.mkstemp()
    with open(fname, 'w+b') as fd:
        fd.write(b'Hello content!')

    return fname


def test_upload_attachment(ctx, attachment_file):
    # Get current attachment count
    resp = requests.get(ctx.base_url+'/rest/api/2/issue/KT-5',
                        auth=ctx.admin_auth)
    assert resp.status_code == 200
    current = len(resp.json()['fields']['attachment'])

    # Upload attachment
    attachment = {
      'file': open(attachment_file, 'rb')
    }

    resp = requests.post(ctx.base_url+'/rest/api/2/issue/KT-5/attachments',
                         auth=ctx.admin_auth,
                         headers=NOCHECK,
                         files=attachment)
    assert resp.status_code == 200

    # Get new attachement count
    resp = requests.get(ctx.base_url+'/rest/api/2/issue/KT-5',
                        auth=ctx.admin_auth)
    assert resp.status_code == 200
    newcount = len(resp.json()['fields']['attachment'])

    assert newcount == current + 1
