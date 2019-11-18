#!/usr/bin/python3

from entrypoint_helpers import env, gen_cfg, gen_container_id, start_app


RUN_USER = env['run_user']
RUN_GROUP = env['run_group']
JIRA_INSTALL_DIR = env['jira_install_dir']
JIRA_HOME = env['jira_home']

gen_cfg('server.xml.j2', f'{JIRA_INSTALL_DIR}/conf/server.xml')
gen_cfg('container_id.j2', '/etc/container_id')
gen_cfg('dbconfig.xml.j2', f'{JIRA_HOME}/dbconfig.xml',
        user=RUN_USER, group=RUN_GROUP, overwrite=False)
gen_cfg('cluster.properties.j2', f'{JIRA_HOME}/cluster.properties',
        user=RUN_USER, group=RUN_GROUP, overwrite=False)

start_app(f'{JIRA_INSTALL_DIR}/bin/start-jira.sh -fg', JIRA_HOME, name='Jira')
