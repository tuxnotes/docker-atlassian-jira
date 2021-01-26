#!/usr/bin/python3 -B

import os
import tempfile

from entrypoint_helpers import env, gen_cfg, gen_container_id, str2bool, start_app


RUN_USER = env['run_user']
RUN_GROUP = env['run_group']
JIRA_INSTALL_DIR = env['jira_install_dir']
JIRA_HOME = env['jira_home']

def replace_key(filename, key, value):
    with open(filename, 'rU') as f_in, tempfile.NamedTemporaryFile(
            'w', dir=os.path.dirname(filename), delete=False) as f_out:
        for line in f_in.readlines():
            if line.startswith(key):
                line = '='.join((line.split('=')[0], '{}\n'.format(value)))
            f_out.write(line)
    os.unlink(filename)
    os.rename(f_out.name, filename)

gen_container_id()
if os.stat('/etc/container_id').st_size == 0:
    gen_cfg('container_id.j2', '/etc/container_id',
            user=RUN_USER, group=RUN_GROUP, overwrite=True)
gen_cfg('server.xml.j2', f'{JIRA_INSTALL_DIR}/conf/server.xml')
gen_cfg('seraph-config.xml.j2',
        f'{JIRA_INSTALL_DIR}/atlassian-jira/WEB-INF/classes/seraph-config.xml')
gen_cfg('dbconfig.xml.j2', f'{JIRA_HOME}/dbconfig.xml',
        user=RUN_USER, group=RUN_GROUP, overwrite=False)
if str2bool(env.get('clustered')):
    fileExists = os.path.exists(f'{JIRA_HOME}/cluster.properties')

    if fileExists and env.get('ehcache_listener_hostname') is not None:
        replace_key(f'{JIRA_HOME}/cluster.properties', 'ehcache.listener.hostName',
                    env.get('ehcache_listener_hostname'))
    elif not fileExists:
        gen_cfg('cluster.properties.j2', f'{JIRA_HOME}/cluster.properties',
                user=RUN_USER, group=RUN_GROUP, overwrite=False)

start_app(f'{JIRA_INSTALL_DIR}/bin/start-jira.sh -fg', JIRA_HOME, name='Jira')
