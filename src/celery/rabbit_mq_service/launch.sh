#!/bin/bash

rabbitmqctl add_user $RABBITMQ_USER $RABBITMQ_PASSWORD
rabbitmqctl set_user_tags $RABBITMQ_USER administrator
rabbitmqctl add_vhost $RABBITMQ_VHOST
rabbitmqctl set_user_tags $RABBITMQ_USER $RABBITMQ_TAG
rabbitmqctl set_permissions -p $RABBITMQ_VHOST $RABBITMQ_USER ".*" ".*" ".*"

rabbitmq-server start