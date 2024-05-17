#!/bin/bash
set -e


psql -U postgres -c "CREATE DATABASE $DB_NAME;"
psql -U postgres -c "CREATE ROLE $DB_USER WITH PASSWORD '$DB_PASSWORD';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
psql -U postgres -c "ALTER ROLE $DB_USER WITH LOGIN;"
psql -U postgres -d $DB_NAME -c "GRANT ALL PRIVILEGES ON SCHEMA public TO $DB_USER;"

psql -U postgres -c "CREATE DATABASE $DB_NAME_TWO;"
psql -U postgres -c "CREATE ROLE $DB_USER_TWO WITH PASSWORD '$DB_PASSWORD_TWO';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME_TWO TO $DB_USER_TWO;"
psql -U postgres -c "ALTER ROLE $DB_USER_TWO WITH LOGIN;"
psql -U postgres -d $DB_NAME_TWO -c "GRANT ALL PRIVILEGES ON SCHEMA public TO $DB_USER_TWO;"