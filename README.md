# ePass #

### REQUIREMENTS ###

* Python 3.10+ - https://www.python.org/downloads/
* Redis - https://redis.io/
* Postgres - https://www.postgresql.org
* Docker (optional) - https://www.docker.com/

### Local Start ###

* Create Postgres DB:
```commandline
CREATE DATABASE epass_db;
CREATE ROLE epass_username with password "password";
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

```commandline
docker-compose build
docker-compose up
```