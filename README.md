![Atlassian JIRA](https://www.atlassian.com/dam/wac/legacy/jira_logo_landing.png)

JIRA Software is a software development tool used by agile teams.

Learn more about JIRA Software: <https://www.atlassian.com/software/jira>

# Overview

This Docker container makes it easy to get an instance of JIRA Software up and running.

# Quick Start

For the `JIRA_HOME` directory that is used to store application data (amongst other things) we recommend mounting a host directory as a [data volume](https://docs.docker.com/engine/tutorials/dockervolumes/#/data-volumes), or via a named volume if using a docker version >= 1.9. 

To get started you can use a data volume, or named volumes. In this example we'll use named volumes.

    $> docker volume create --name jiraVolume
    $> docker run -v jiraVolume:/var/atlassian/application-data/jira --name="jira" -d -p 8080:8080 dchevell/jira-software


**Success**. JIRA is now available on [http://localhost:8080](http://localhost:8080)*

Please ensure your container has the necessary resources allocated to it. We recommend 2GiB of memory allocated to accommodate the application server. See [System Requirements](https://confluence.atlassian.com/adminjiraserver071/jira-applications-installation-requirements-802592164.html) for further information.
    

_* Note: If you are using `docker-machine` on Mac OS X, please use `open http://$(docker-machine ip default):8080` instead._

## Memory / Heap Size

If you need to override JIRA's default memory allocation, you can control the minimum heap (Xms) and maximum heap (Xmx) via the below environment variables.

* `JVM_MINIMUM_MEMORY` (default: 384m)

   The minimum heap size of the JVM

* `JVM_MAXIMUM_MEMORY` (default: 768m)

   The maximum heap size of the JVM

## Reverse Proxy Settings

If JIRA is run behind a reverse proxy server as [described here](https://confluence.atlassian.com/adminjiraserver072/integrating-jira-with-apache-using-ssl-828788158.html), then you need to specify extra options to make JIRA aware of the setup. They can be controlled via the below environment variables.

* `CATALINA_CONNECTOR_PROXYNAME` (default: NONE)

   The reverse proxy's fully qualified hostname.

* `CATALINA_CONNECTOR_PROXYPORT` (default: NONE)

   The reverse proxy's port number via which JIRA is accessed.

* `CATALINA_CONNECTOR_SCHEME` (default: http)

   The protocol via which JIRA is accessed.

* `CATALINA_CONNECTOR_SECURE` (default: false)

   Set 'true' if CATALINA_CONNECTOR_SCHEME is 'https'.

## JVM configuration

If you need to pass additional JVM arguments to JIRA, such as specifying a custom trust store, you can add them via the below environment variable

* `JVM_SUPPORT_RECOMMENDED_ARGS`

   Additional JVM arguments for JIRA
   
Example:

    $> docker run -e JVM_SUPPORT_RECOMMENDED_ARGS=-Djavax.net.ssl.trustStore=/var/atlassian/application-data/jira/cacerts -v jiraVolume:/var/atlassian/application-data/jira --name="jira" -d -p 8080:8080 dchevell/jira-software
    
# Upgrade

To upgrade to a more recent version of JIRA you can simply stop the `jira` container and start a new one based on a more recent image:

    $> docker stop jira
    $> docker rm jira
    $> docker run ... (See above)

As your data is stored in the data volume directory on the host it will still  be available after the upgrade.

_Note: Please make sure that you **don't** accidentally remove the `jira` container and its volumes using the `-v` option._

# Backup

For evaluations you can use the built-in database that will store its files in the JIRA home directory. In that case it is sufficient to create a backup archive of the docker volume.

If you're using an external database, you can configure JIRA to make a backup automatically each night. This will back up the current state, including the database to the `jiraVolume` docker volume, which can then be archived. Alternatively you can backup the database separately, and continue to create a backup archive of the docker volume to back up the JIRA Home directory.

Read more about data recovery and backups: [https://confluence.atlassian.com/adminjiraserver071/backing-up-data-802592964.html](https://confluence.atlassian.com/adminjiraserver071/backing-up-data-802592964.html)

# Versioning

The `latest` tag matches the most recent release of Atlassian JIRA Software. Thus `dchevell/jira-software:latest` will use the newest version of JIRA available.

Alternatively you can use a specific major, major.minor, or major.minor.patch version of JIRA Software by using a version number tag: 

* `dchevell/jira-software:7`
* `dchevell/jira-software:7.5`
* `dchevell/jira-software:7.5.0`

All versions from 7.0+ are available

# Support

This Docker container is unsupported and is intended for illustration purposes only.