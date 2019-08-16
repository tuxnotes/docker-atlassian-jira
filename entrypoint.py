#!/usr/bin/python3

import sys
import os
import shutil
import logging
import jinja2 as j2


######################################################################
# Utils

logging.basicConfig(level=logging.DEBUG)

def set_perms(path, user, group, mode):
    shutil.chown(path, user=user, group=group)
    os.chmod(path, mode)

# Setup Jinja2 for templating
jenv = j2.Environment(
    loader=j2.FileSystemLoader('/opt/atlassian/etc/'),
    autoescape=j2.select_autoescape(['xml']))

def gen_cfg(tmpl, target, env, user='root', group='root', mode=0o644):
    logging.info(f"Generating {target} from template {tmpl}")
    cfg = jenv.get_template(tmpl).render(env)
    with open(target, 'w') as fd:
        fd.write(cfg)
    set_perms(target, user, group, mode)


######################################################################
# Setup inputs and outputs

# Import all ATL_* and Dockerfile environment variables. We lower-case
# these for compatability with Ansible template convention. We also
# support CATALINA variables from older versions of the Docker images
# for backwards compatability, if the new version is not set.
env = {k.lower(): v
       for k, v in os.environ.items()
       if k.startswith(('ATL_', 'JIRA_', 'RUN_', 'CATALINA_'))}


######################################################################
# Generate all configuration files for Jira

gen_cfg('server.xml.j2',
        f"{env['jira_install_dir']}/conf/server.xml", env)

gen_cfg('dbconfig.xml.j2',
        f"{env['jira_home']}/dbconfig.xml", env)


######################################################################
# Start Jira as the correct user

start_cmd = f"{env['jira_install_dir']}/bin/start-jira.sh"
if os.getuid() == 0:
    logging.info(f"User is currently root. Will change directory ownership to {env['run_user']} then downgrade permissions")
    set_perms(env['jira_home'], env['run_user'], env['run_group'], 0o700)

    cmd = '/bin/su'
    start_cmd = ' '.join([start_cmd] + sys.argv[1:])
    args = [cmd, env['run_user'], '-c', start_cmd]
else:
    cmd = start_cmd
    args = [start_cmd] + sys.argv[1:]

logging.info(f"Running Jira with command '{cmd}', arguments {args}")
os.execv(cmd, args)
