#!/bin/bash

envsubst < /consul/config_template.json > /etc/consul/config.json

/usr/bin/supervisord --nodaemon
