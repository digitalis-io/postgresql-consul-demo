#!/bin/bash

envsubst < /consul/config_template.json > /etc/consul/config.json

chown pgbouncer:pgbouncer /etc/pgbouncer/*

/usr/bin/supervisord --nodaemon
