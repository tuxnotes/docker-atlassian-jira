from jinja2 import Template
from pathlib import Path
import os

TEMPLATE_FILE = 'bitbucket-pipelines.yml.j2'

DOCKERFILE_VERSION_ARG='JIRA_VERSION'

images = {
    'software': {
        8: {
            start_version: '7.13',
            end_version: '9',
            default_release: True,
            extra_tag_suffixes: ['ubuntu']
        },
        11: {
            start_version: '8.2',
            end_version: '9',
            default_release: False,
            base_image: 'adoptopenjdk:11-hotspot',
        }
    },
    'servicedesk': {
        docker_repos: ['atlassian/jira-servicemanagement', 'atlassian/jira-servicedesk'],
        8: {
            start_version: '3.16',
            end_version: '5',
            default_release: True,
            extra_tag_suffixes: ['ubuntu']
        },
        11: {
            start_version: '4.2',
            end_version: '5',
            default_release: False,
        }
    },
    'core': {
        8: {
            start_version: '7.13',
            end_version: '9',
            default_release: True,
            extra_tag_suffixes: ['ubuntu']
        },
        11: {
            start_version: '8.2',
            end_version: '9',
            default_release: False,
            base_image: 'adoptopenjdk:11-hotspot',
        }
    }
}



def main():
    path = Path(os.path.join(os.path.dirname(__file__), TEMPLATE_FILE))
    template = Template(path.read_text())
    generated_output = template.render(flavours=images)

    print(generated_output)

if __name__ == '__main__':
    main()
