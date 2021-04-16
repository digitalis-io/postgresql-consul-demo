#!/bin/bash

envsubst < /consul/config_template.json > /etc/consul/config.json
envsubst < /etc/patroni/patroni_template.yml > /etc/patroni/postgres.yml

/usr/bin/supervisord --nodaemon
