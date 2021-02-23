#!/usr/bin/python3

from jinja2 import Template
from pathlib import Path
import os

TEMPLATE_FILE = 'bitbucket-pipelines.yml.j2'

DOCKERFILE_VERSION_ARG='JIRA_VERSION'

CORE_REPOS = ['atlassian/jira-core']
SOFTWARE_REPOS = ['atlassian/jira-software']
SD_REPOS = ['atlassian/jira-servicemanagement', 'atlassian/jira-servicedesk']

images = {
    'Jira Software': {
        8: {
            'mac_key': 'jira-software',
            'start_version': '7.13',
            'end_version': '9',
            'default_release': True,
            'extra_tag_suffixes': ['ubuntu'],
            'docker_repos': SOFTWARE_REPOS,
        },
        11: {
            'mac_key': 'jira-software',
            'start_version': '8.2',
            'end_version': '9',
            'default_release': False,
            'base_image': 'adoptopenjdk:11-hotspot',
            'docker_repos': SOFTWARE_REPOS,
        }
    },
    'Jira Service Management': {
        8: {
            'mac_key': 'jira-servicedesk',
            'start_version': '3.16',
            'end_version': '5',
            'default_release': True,
            'extra_tag_suffixes': ['ubuntu'],
            'docker_repos': SD_REPOS,
        },
        11: {
            'mac_key': 'jira-servicedesk',
            'start_version': '4.2',
            'end_version': '5',
            'default_release': False,
            'docker_repos': SD_REPOS,
        }
    },
    'Jira Core': {
        8: {
            'mac_key': 'jira',
            'start_version': '7.13',
            'end_version': '9',
            'default_release': True,
            'extra_tag_suffixes': ['ubuntu'],
            'docker_repos': CORE_REPOS,
        },
        11: {
            'mac_key': 'jira',
            'start_version': '8.2',
            'end_version': '9',
            'default_release': False,
            'base_image': 'adoptopenjdk:11-hotspot',
            'docker_repos': CORE_REPOS,
        }
    }
}


def main():
    path = Path(os.path.join(os.path.dirname(__file__), TEMPLATE_FILE))
    template = Template(path.read_text())
    generated_output = template.render(images=images)

    print(generated_output)

if __name__ == '__main__':
    main()
