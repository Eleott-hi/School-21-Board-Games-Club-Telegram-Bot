FROM postgres:16


ENV DB_NAME=prod_db
ENV DB_USER=prod_user
ENV DB_PASSWORD=prod_password

ENV DB_NAME_TWO=test_db
ENV DB_USER_TWO=test_user
ENV DB_PASSWORD_TWO=test_passw

COPY ./init_db.sh /docker-entrypoint-initdb.d/

RUN chmod +x /docker-entrypoint-initdb.d/init_db.sh

EXPOSE 5432
