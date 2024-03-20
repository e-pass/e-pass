# ePass #

### Overview ###
E-pass caters to a wide range of activities beyond the classroom, such as tutoring sessions, sports sections, and other extracurricular programs. The application offers a user-friendly interface for organizers to manage subscriptions and track attendance, while participants can effortlessly stay informed about their schedules and receive updates.

### Tech Stack ###
- Django;
- Django Rest Framework;
- Postgres DB;
- Redis

### REQUIREMENTS ###

* Python 3.10+ - https://www.python.org/downloads/
* Redis - https://redis.io/
* Postgres - https://www.postgresql.org
* Docker (optional) - https://www.docker.com/

### Local Start ###

* Create Postgres DB:
```commandline
CREATE DATABASE epass_db;
CREATE ROLE epass_username with password 'password';
ALTER ROLE "epass_username" with LOGIN;
GRANT ALL PRIVILEGES ON DATABASE "epass_db" TO epass_username;
ALTER USER epass_username CREATEDB;
```
* Install requirements and start server:
```commandline
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```
* Start Redis
* Start Celery:
```commandline
celery -A ePass.celery worker -l INFO
```

### Docker Start ###

* Update .env file

```commandline
docker-compose build
docker-compose up
```

### Pre-commit hook ###
```commandline
pre-commit install
pre-commit run --all-files
```