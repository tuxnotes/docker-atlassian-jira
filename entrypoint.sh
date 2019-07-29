#!/bin/bash
set -euo pipefail

function log {
    echo '[Entrypoint]' $*
}

# Setup Catalina Opts
: ${CATALINA_CONNECTOR_PROXYNAME:=}
: ${CATALINA_CONNECTOR_PROXYPORT:=}
: ${CATALINA_CONNECTOR_SCHEME:=http}
: ${CATALINA_CONNECTOR_SECURE:=false}
: ${CATALINA_CONTEXT_PATH:=}

: ${CATALINA_OPTS:=}

: ${JAVA_OPTS:=}

CATALINA_OPTS="${CATALINA_OPTS} -DcatalinaConnectorProxyName=${CATALINA_CONNECTOR_PROXYNAME}"
CATALINA_OPTS="${CATALINA_OPTS} -DcatalinaConnectorProxyPort=${CATALINA_CONNECTOR_PROXYPORT}"
CATALINA_OPTS="${CATALINA_OPTS} -DcatalinaConnectorScheme=${CATALINA_CONNECTOR_SCHEME}"
CATALINA_OPTS="${CATALINA_OPTS} -DcatalinaConnectorSecure=${CATALINA_CONNECTOR_SECURE}"
CATALINA_OPTS="${CATALINA_OPTS} -DcatalinaContextPath=${CATALINA_CONTEXT_PATH}"

export JAVA_OPTS="${JAVA_OPTS} ${CATALINA_OPTS}"

# Setup Data Center configuration
if [ ! -s "/etc/container_id" ]; then
    uuidgen > /etc/container_id
fi
CONTAINER_ID=$(cat /etc/container_id)
CONTAINER_SHORT_ID=${CONTAINER_ID::8}

: ${CLUSTERED:=false}
: ${JIRA_NODE_ID:=jira_node_${CONTAINER_SHORT_ID}}
: ${JIRA_SHARED_HOME:=${JIRA_HOME}/shared}
: ${EHCACHE_PEER_DISCOVERY:=}
: ${EHCACHE_LISTENER_HOSTNAME:=}
: ${EHCACHE_LISTENER_PORT:=}
: ${EHCACHE_LISTENER_SOCKETTIMEOUTMILLIS:=}
: ${EHCACHE_MULTICAST_ADDRESS:=}
: ${EHCACHE_MULTICAST_PORT:=}
: ${EHCACHE_MULTICAST_TIMETOLIVE:=}
: ${EHCACHE_MULTICAST_HOSTNAME:=}

# Cleanly set/unset values in cluster.properties
function set_cluster_property {
    if [ -z $2 ]; then
        if [ -f "${JIRA_HOME}/cluster.properties" ]; then
            sed -i -e "/^${1}/d" "${JIRA_HOME}/cluster.properties"
        fi
        return
    fi
    if [ ! -f "${JIRA_HOME}/cluster.properties" ]; then
        echo "${1}=${2}" >> "${JIRA_HOME}/cluster.properties"
    elif grep "^${1}" "${JIRA_HOME}/cluster.properties"; then
        sed -i -e "s#^${1}=.*#${1}=${2}#g" "${JIRA_HOME}/cluster.properties"
    else
        echo "${1}=${2}" >> "${JIRA_HOME}/cluster.properties"
    fi
}

if [ "${CLUSTERED}" == "true" ]; then
    log "Generating ${JIRA_HOME}/cluster.properties"
    set_cluster_property "jira.node.id" "${JIRA_NODE_ID}"
    set_cluster_property "jira.shared.home" "${JIRA_SHARED_HOME}"
    set_cluster_property "ehcache.peer.discovery" "${EHCACHE_PEER_DISCOVERY}"
    set_cluster_property "ehcache.listener.hostName" "${EHCACHE_LISTENER_HOSTNAME}"
    set_cluster_property "ehcache.listener.port" "${EHCACHE_LISTENER_PORT}"
    set_cluster_property "ehcache.listener.socketTimeoutMillis" "${EHCACHE_LISTENER_PORT}"
    set_cluster_property "ehcache.multicast.address" "${EHCACHE_MULTICAST_ADDRESS}"
    set_cluster_property "ehcache.multicast.port" "${EHCACHE_MULTICAST_PORT}"
    set_cluster_property "ehcache.multicast.timeToLive" "${EHCACHE_MULTICAST_TIMETOLIVE}"
    set_cluster_property "ehcache.multicast.hostName" "${EHCACHE_MULTICAST_HOSTNAME}"
fi


# Setup dbconfig.xml if the database details have been passed in.
: ${ATL_JDBC_URL:=}

if [[ ! -z "$ATL_JDBC_URL" ]]; then
    # Generate the template variables. We lower-case these vars to be
    # compatible with the Ansible templates in
    # https://bitbucket.org/atlassian/dc-deployments-automation

    # Must be supplied
    export atl_jdbc_url=${ATL_JDBC_URL}
    export atl_db_driver=${ATL_DB_DRIVER}
    export atl_jdbc_user=${ATL_JDBC_USER}
    export atl_jdbc_password=${ATL_JDBC_PASSWORD}

    # Defaults, can be overridden
    export atl_db_maxidle=${ATL_DB_MAXIDLE:=20}
    export atl_db_maxwaitmillis=${ATL_DB_MAXWAITMILLIS:=30000}
    export atl_db_minevictableidletimemillis=${ATL_DB_MINEVICTABLEIDLETIMEMILLIS:=5000}
    export atl_db_minidle=${ATL_DB_MINIDLE:=10}
    export atl_db_poolmaxsize=${ATL_DB_POOLMAXSIZE:=100}
    export atl_db_poolminsize=${ATL_DB_POOLMINSIZE:=20}
    export atl_db_removeabandoned=${ATL_DB_REMOVEABANDONED:=true}
    export atl_db_removeabandonedtimeout=${ATL_DB_REMOVEABANDONEDTIMEOUT:=300}
    export atl_db_testonborrow=${ATL_DB_TESTONBORROW:=false}
    export atl_db_testwhileidle=${ATL_DB_TESTWHILEIDLE:=true}
    export atl_db_timebetweenevictionrunsmillis=${ATL_DB_TIMEBETWEENEVICTIONRUNSMILLIS:=30000}

    /opt/atlassian/bin/templater.sh \
        /opt/atlassian/etc/dbconfig.xml.j2 \
        > ${JIRA_HOME}/dbconfig.xml
fi



# Start Jira as the correct user
if [ "${UID}" -eq 0 ]; then
    log "User is currently root. Will change directory ownership to ${RUN_USER}:${RUN_GROUP}, then downgrade permission to ${RUN_USER}"
    PERMISSIONS_SIGNATURE=$(stat -c "%u:%U:%a" "${JIRA_HOME}")
    EXPECTED_PERMISSIONS=$(id -u ${RUN_USER}):${RUN_USER}:700
    if [ "${PERMISSIONS_SIGNATURE}" != "${EXPECTED_PERMISSIONS}" ]; then
        chmod -R 700 "${JIRA_HOME}" &&
            chown -R "${RUN_USER}:${RUN_GROUP}" "${JIRA_HOME}"
    fi
    # Now drop privileges
    exec su -s /bin/bash "${RUN_USER}" -c "$JIRA_INSTALL_DIR/bin/start-jira.sh $@"
else
    exec "$JIRA_INSTALL_DIR/bin/start-jira.sh" "$@"
fi
