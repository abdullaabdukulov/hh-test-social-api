#!/bin/bash

chmod +x start.sh
./start.sh test
# echo "export $PROJECT_NAME
# export $DJANGO_SETTINGS_MODULE
# export $SECRET_KEY
# export $DB_NAME
# export $DB_HOST
# export $DB_PORT
# export $DB_USER
# export $DB_PASSWORD
# export $REDIS_HOST
# export $REDIS_PORT
# export $CELERY_FLOWER_USER
# export $CELERY_FLOWER_PASSWORD
docker compose up -d --build
docker system prune -fa