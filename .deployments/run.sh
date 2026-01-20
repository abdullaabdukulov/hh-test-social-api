#!/bin/bash

set -e

cd /code

if [ $# -eq 0 ]; then
    echo "Usage: start.sh [PROCESS_TYPE](app/beat/worker/flower/test)"
    exit 1
fi

PROCESS_TYPE=$1

case $PROCESS_TYPE in
    app)
        python manage.py collectstatic --noinput
        python manage.py migrate
        gunicorn \
            --bind 0.0.0.0:8000 \
            --workers 4 \
            --timeout 300 \
            --graceful-timeout 10 \
            --log-level info \
            --access-logfile "-" \
            --error-logfile "-" \
            config.wsgi:application

        exit 0
        ;;

    worker)
        celery \
            --app config \
            worker \
            --loglevel INFO

        exit 0
        ;;

    beat)
        celery \
            --app config \
            beat \
            --loglevel INFO \
            --scheduler /tmp/celerybeat-schedule

        exit 0
        ;;

    flower)
        celery \
            --app config \
            flower \
            --address=0.0.0.0 \
            --port=5555 \
            --url_prefix=flower \
            --loglevel INFO

        exit 0
        ;;

    test)
        python manage.py migrate
        python manage.py test
        exit 0
        ;;
esac

exec "$@"
