
from functools import reduce
import logging
import pytest
import requests


def test_status(ctx):
    resp = requests.get(ctx.base_url+'/status')
    assert resp.status_code == 200
    assert resp.json()['state'] == "RUNNING"


def test_plugins(ctx):
    sysinfo = requests.get(ctx.base_url+'/rest/api/2/serverInfo/', auth=ctx.admin_auth)
    assert sysinfo.status_code == 200
    version = sysinfo.json()['version']
    if int(version.split(".")[0]) >= 0:
        return
    resp = requests.get(ctx.base_url+'/rest/plugins/1.0/', auth=ctx.admin_auth)
    assert resp.status_code == 200
    plugins = resp.json()['plugins']
    # We shouldn't rely on precise number of plugins as this is subject to change
    assert len(plugins) > 200
    # ... but all of the plugins should be enabled
    assert reduce(lambda a, b: a and b, map(lambda x: x['enabled'], plugins))


def test_valid_index(ctx):
    # The system is reindexed on startup; see the reindex_before_tests fixture
    resp = requests.get(
        ctx.base_url+'/rest/api/2/index/summary', auth=ctx.admin_auth)
    assert resp.status_code == 200
    idx = resp.json()['issueIndex']
    assert idx['indexReadable']
    dbcount = idx['countInDatabase']
    idxcount = idx['countInIndex']

    assert dbcount > 0
    assert idxcount == dbcount
