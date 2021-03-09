
from datetime import datetime
from functools import reduce
import json
import logging
import pytest
import requests


def test_valid_index(ctx):
    resp = requests.get(ctx.base_url+'/rest/api/2/issue/KT-1',
                        auth=ctx.admin_auth)
    assert resp.status_code == 200
    issue = resp.json()
    assert issue['fields']['summary'].startswith('Kanban cards represent work items >> Click the "KT-1" link')


def test_create_issue(ctx):
    issue = {
      'fields': {
        'project': { 'key': "KT" },
        'summary': "New ticket" + str(datetime.now()),
        'issuetype': { 'name': "Task" }
      }
    }

    resp = requests.post(ctx.base_url+'/rest/api/2/issue',
                         auth=ctx.admin_auth,
                         json=json.dumps(issue))
    assert resp.status_code == 201


def test_jql(ctx):
    resp = requests.get(ctx.base_url+'/rest/api/2/search?jql=assignee=admin',
                        auth=ctx.admin_auth)
    assert resp.status_code == 200
    assert resp.json()['total'] == 16


@pytest.fixture(scope='session')
def transition_ids(ctx):
    resp = requests.get(ctx.base_url+'/rest/api/2/issue/KT-10/transitions',
                        auth=ctx.admin_auth)
    assert resp.status_code == 200
    trns = resp.json()['transitions']
    current = list(filter(lambda x: x['name'] == 'Done', trns))[0]['id']
    target = list(filter(lambda x: x['name'] == 'In Progress', trns))[0]['id']
    return {
        'current': current,
        'target': target
    }

# Move the issue back to Done so the test is idempotent
def reset_kt10(ctx, transition_ids):
    trn = {
        'transition': { 'id': transition_ids['current'] }
    }

    resp = requests.post(ctx.base_url+'/rest/api/2/issue/KT-10/transitions',
                         auth=ctx.admin_auth,
                         json=json.dumps(trn))
    assert resp.status_code == 204


def test_done_inprogress(ctx, transition_ids):
    reset_kt10(ctx, transition_ids)

    trn = {
        'transition': { 'id': transition_ids['target'] }
    }

    resp = requests.post(ctx.base_url+'/rest/api/2/issue/KT-10/transitions',
                         auth=ctx.admin_auth,
                         json=json.dumps(trn))
    assert resp.status_code == 204

    reset_kt10(ctx, transition_ids)
