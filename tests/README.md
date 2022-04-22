# Overview

This folder contains unit tests for Jira image. 

## How to run tests locally
To run tests locally, we need pipenv to create a virtual environment. To install it on mac: 
```
brew install pipenv
```


Then install required packages. (Note that for local testing, we'll be using requirements-3.9.txt) 
```
pipenv install -r shared-components/tests/requirements-3.9.txt
```

Set the required environment variables:
```
export DOCKERFILE='Dockerfile'
export DOCKERFILE_BUILDARGS='ARTEFACT_NAME=atlassian-jira-software'
export DOCKERFILE_VERSION_ARG='JIRA_VERSION'
export MAC_PRODUCT_KEY='jira-software'
```

To run the tests, 
```
pipenv run py.test -v tests
```

After all tests are passed, you can safely remove the virtual environment. 
```
pipenv --rm
```

