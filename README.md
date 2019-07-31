![Atlassian JIRA](https://wac-cdn.atlassian.com/dam/jcr:e348b562-4152-4cdc-8a55-3d297e509cc8/Jira%20Software-blue.svg?cdnVersion=le)

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

If JIRA is run behind a reverse proxy server (e.g. a load-balancer or nginx server) as 
[described here](https://confluence.atlassian.com/adminjiraserver072/integrating-jira-with-apache-using-ssl-828788158.html),
then you need to specify extra options to make JIRA aware of the setup. They can
be controlled via the below environment variables.

* `ATL_PROXY_NAME` (default: NONE)

   The reverse proxy's fully qualified hostname. `CATALINA_CONNECTOR_PROXYNAME`
   is also supported for backwards compatability.

* `ATL_PROXY_PORT` (default: NONE)

   The reverse proxy's port number via which JIRA is
   accessed. `CATALINA_CONNECTOR_PROXYPORT` is also supported for backwards
   compatability.

* `ATL_TOMCAT_SCHEME` (default: http)

   The protocol via which JIRA is accessed. `CATALINA_CONNECTOR_SCHEME` is also
   supported for backwards compatability.

* `ATL_TOMCAT_SECURE` (default: false)

   Set 'true' if `ATL_TOMCAT_SCHEME` is 'https'. `CATALINA_CONNECTOR_SECURE` is
   also supported for backwards compatability.

* `ATL_TOMCAT_CONTEXTPATH` (default: NONE)

   The context path the application is served over. `CATALINA_CONTEXT_PATH` is
   also supported for backwards compatability.

The following Tomcat/Catalina options are also supported. For more information,
see https://tomcat.apache.org/tomcat-7.0-doc/config/index.html.

* `ATL_TOMCAT_PORT` (default: 8080)
* `ATL_TOMCAT_MGMT_PORT` (default: 8005)
* `ATL_TOMCAT_MAXTHREADS` (default: 200)
* `ATL_TOMCAT_MINSPARETHREADS` (default: 10)
* `ATL_TOMCAT_CONNECTIONTIMEOUT` (default: 20000)
* `ATL_TOMCAT_ENABLELOOKUPS` (default: false)
* `ATL_TOMCAT_PROTOCOL` (default: HTTP/1.1)
* `ATL_TOMCAT_ACCEPTCOUNT` (default: 10)

## JVM configuration

If you need to pass additional JVM arguments to JIRA, such as specifying a custom trust store, you can add them via the below environment variable

* `JVM_SUPPORT_RECOMMENDED_ARGS`

   Additional JVM arguments for JIRA

Example:

    $> docker run -e JVM_SUPPORT_RECOMMENDED_ARGS=-Djavax.net.ssl.trustStore=/var/atlassian/application-data/jira/cacerts -v jiraVolume:/var/atlassian/application-data/jira --name="jira" -d -p 8080:8080 dchevell/jira-software

## Database configuration

It is optionally possible to configure the database from the environment,
avoiding the need to do so through the web startup screen.

The following variables are all must all be supplied if using this feature:

* `ATL_JDBC_URL`

   The database URL; this is database-specific.

* `ATL_JDBC_USER`

   The database user to connect as.

* `ATL_JDBC_PASSWORD`

   The password for the database user.

* `ATL_DB_DRIVER`

   The JDBC driver class; supported drivers are:

   * `com.microsoft.sqlserver.jdbc.SQLServerDriver`
   * `com.mysql.jdbc.Driver`
   * `oracle.jdbc.OracleDriver`
   * `org.postgresql.Driver`
   
   The driver must match the DB type (see next entry).

* `ATL_DB_TYPE`

   The type of database; valid supported values are:

   * `mssql`
   * `mysql`
   * `oracle10g`
   * `postgres72`

The following variables are for the Tomcat JDBC connection pool, and are
optional. For more information on these see: https://tomcat.apache.org/tomcat-7.0-doc/jdbc-pool.html

* `ATL_DB_MAXIDLE` (default: 20)
* `ATL_DB_MAXWAITMILLIS` (default: 30000)
* `ATL_DB_MINEVICTABLEIDLETIMEMILLIS` (default: 5000)
* `ATL_DB_MINIDLE` (default: 10)
* `ATL_DB_POOLMAXSIZE` (default: 100)
* `ATL_DB_POOLMINSIZE` (default: 20)
* `ATL_DB_REMOVEABANDONED` (default: true)
* `ATL_DB_REMOVEABANDONEDTIMEOUT` (default: 300)
* `ATL_DB_TESTONBORROW` (default: false)
* `ATL_DB_TESTWHILEIDLE` (default: true)
* `ATL_DB_TIMEBETWEENEVICTIONRUNSMILLIS` (default: 30000)


## Data Center configuration

This docker image can be run as part of a [Data Center](https://confluence.atlassian.com/enterprise/jira-data-center-472219731.html) cluster. You can specify the following properties to start Jira as a Data Center node, instead of manually configuring a cluster.properties file, See [Installing Jira Data Center](https://confluence.atlassian.com/adminjiraserver071/installing-jira-data-center-802592197.html) for more information on each property and its possible configuration.

* `CLUSTERED` (default: false)

   Set 'true' to enable clustering configuration to be used. This will create a **cluster.properties** file inside the container's `$JIRA_HOME` directory.

* `JIRA_NODE_ID` (default: jira_node_<container-id>)

   The unique ID for the node. By default, this includes a randomly generated ID unique to each container, but can be overridden with a custom value.

* `JIRA_SHARED_HOME` (default: $JIRA_HOME/shared)

   The location of the shared home directory for all Jira nodes.

* `EHCACHE_PEER_DISCOVERY` (default: default)

   Describes how nodes find each other.

* `EHCACHE_LISTENER_HOSTNAME` (default: NONE)

   The hostname of the current node for cache communication. Jira Data Center will resolve this this internally if the parameter isn't set.

* `EHCACHE_LISTENER_PORT` (default: 40001)

   The port the node is going to be listening to.

* `EHCACHE_LISTENER_SOCKETTIMEOUTMILLIS` (default: 2000)

   The default timeout for the Ehcache listener.

* `EHCACHE_MULTICAST_ADDRESS` (default: NONE)

   A valid multicast group address. Required when EHCACHE_PEER_DISCOVERY is set to 'automatic' insted of 'default'.

* `EHCACHE_MULTICAST_PORT` (default: NONE)

   The dedicated port for the multicast heartbeat traffic.Required when EHCACHE_PEER_DISCOVERY is set to 'automatic' insted of 'default'.

* `EHCACHE_MULTICAST_TIMETOLIVE` (default: NONE)

   A value between 0 and 255 which determines how far the packets will propagate. Required when EHCACHE_PEER_DISCOVERY is set to 'automatic' insted of 'default'.

* `EHCACHE_MULTICAST_HOSTNAME` (default: NONE)

   The hostname or IP of the interface to be used for sending and receiving multicast packets. Required when EHCACHE_PEER_DISCOVERY is set to 'automatic' insted of 'default'.

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
