# Applifting Exercise Readme

## Setup

### Django Environment

1. Create python virtual environment inside root folder of microservice and enable it
   ```bash
   # create
   $ virtualenv .venv

   # enable
   $ source .venv/bin/activate
   ```
2. Install required packages
   ```bash
   $ pip install -r requirements.txt
   ```

### Environment variable file
1. Create an environment variable file called .env in the project folder (product_ms/) 
2. Place the following variables in this file.

```bash

DATABASE_NAME=name_of_db_for_this_ms
DATABASE_USER=user_name_for_db_server
DATABASE_PASS=users_pass_for_db
DATABASE_HOST=address_of_your_db_server
DATABASE_PORT=default_for_postgres_db: 5432
SECRET_KEY=some_secure_string
BASEURL= https://applifting-python-excercise-ms.herokuapp.com/api/v1

```

### Setup Database

1. Create a database for products microservice
2. Run Migrations in virtual environment

```bash
$ python manage.py migrate
```

### Run Server 🤟

```bash
#django server
$ python manage.py runserver
```

3. At this time, we need to authenticate Product MS to Offers MS. We approach this by visiting our */offers/auth/*

```bash
#RabbitMQ message broker
$ rabbitmq-server
#celery periodic tasks to update offers
$ celery -A product_ms worker -B
```

