FROM python:3.10-slim-buster
WORKDIR /app
COPY . /app/
RUN apt update; apt install gcc default-libmysqlclient-dev -y
RUN pip install pipenv
RUN pipenv install --skip-lock
EXPOSE 8000
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]