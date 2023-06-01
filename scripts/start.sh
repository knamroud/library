#!/bin/bash
source .env
if ! [ -z "$1" ]; then
    PRODUCTION=$1
fi
if [ "$PRODUCTION" -eq "0" ]; then
    docker-compose up --no-deps -d backend
else
    mkdir init
    echo 'GRANT USAGE ON \`$DB_NAME\`.* TO \`$DB_USER\`@localhost; GRANT CREATE ON \`$DB_NAME\`.* TO \`$DB_USER\`@localhost;' > init/init.sql
    docker-compose up -d
    sudo rm -rf init
fi