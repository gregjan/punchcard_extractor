#!/bin/bash
set -e

# rabbitmq
if [ "$RABBITMQ_URI" == "" ]; then

    # configure RABBITMQ_URI if started using docker-compose or --link flag
    if [ -n "$RABBITMQ_PORT_5672_TCP_ADDR" ]; then
        RABBITMQ_URI="amqp://${RABBITMQ_PORT_5672_TCP_ADDR}:${RABBITMQ_PORT_5672_TCP_PORT}/%2F"
    fi

    # configure RABBITMQ_URI if rabbitmq is up for kubernetes
    # TODO needs implementation maybe from NDS people
fi

# start server if asked
if [ "$1" = 'extractor' ]; then
    cd /home/clowder

    if [ "$RABBITMQ_PORT_5672_TCP_ADDR" != "" ]; then
        # start extractor after rabbitmq is up
        for i in `seq 1 10`; do
            if nc -z $RABBITMQ_PORT_5672_TCP_ADDR $RABBITMQ_PORT_5672_TCP_PORT ; then
                exec ./${MAIN_SCRIPT}
            fi
            sleep 1
        done
    fi

    # just launch extractor and see what happens
    exec ./${MAIN_SCRIPT}
elif [ "$1" = 'shell' ]; then
  cd /home/clowder
  exec /bin/bash
fi

exec "$@"
