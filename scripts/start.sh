#!/bin/bash
source .env
if [ "$PRODUCTION" -eq "0" ]; then
    docker-compose up --no-deps -d backend
else
    sudo rm -rf mysql
    mkdir init
    echo 'GRANT USAGE ON \`$DB_NAME\`.* TO \`$DB_USER\`@localhost; GRANT CREATE ON \`$DB_NAME\`.* TO \`$DB_USER\`@localhost;' > init/init.sql
    docker-compose up -d
fi
sudo rm -rf init