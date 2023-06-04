FROM python:3.10-slim-buster
WORKDIR /app
COPY . /app/
RUN apt update; apt install gcc default-libmysqlclient-dev mariadb-client nodejs npm -y
RUN npm install -g typescript
RUN pip install pipenv
RUN pipenv install --skip-lock
RUN chmod +x scripts/*
EXPOSE 8000