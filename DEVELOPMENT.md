# Developing Docker images

## Setting up for development

After clonning the repository you will need to clone the submodule:

```
git submodule update --init --force --recursive
```

## Testing

### Pre-requisites

To run the functional testing, you are required to define several variables.

```
JIRA_TEST_LICENSE='license_string' #string with full Jira DC license, don't forget the quotes as the license can contain special characters that would render the license unusable
```

### Run smoke test functional suite


```
export JIRA_VERSION=`curl -s https://marketplace.atlassian.com/rest/2/products/key/jira/versions/latest | jq -r .name`
docker build --build-arg JIRA_VERSION=${JIRA_VERSION} -t jira-test-image .
docker-compose build --build-arg TEST_TARGET_IMAGE=jira-test-image ./func-tests/docker-compose.yaml
./func-tests/run-functests jira-test-image
```

### Develop tests

Install packages

```
cd func-tests/smoketests
yarn install
```

Run the smoke tests

```
cd func-tests
docker-compose up
JIRA_ADMIN_PWD="passwordInLastpass" JIRA_BASEURL="http://localhost:2990/jira" npm test -- --watch
```
