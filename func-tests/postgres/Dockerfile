FROM postgres:10.18-alpine

# NOTE: This expects the license to have been injected; see
# `inject-license` and INJECT_LICENSE_HERE in `jira.sql.tmpl`
COPY jira.sql /docker-entrypoint-initdb.d/jira.sql
