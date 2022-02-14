# RSS Reader API

A REST API that helps users read and follow their favorite RSS Feeds

## API Documentation

[Swagger Documentation](https://rss-feed-api-app.herokuapp.com/)

## Setup

To get the application running on your local environment, run the following commands

- Create a directory and cd into it
- Run `git clone git@github.com:jesseinit/rss_reader_api.git .` to pull the code from Github to your machine
- Create a `.env` file populating it with actual values using the structure in the `.env.sample` file
- Ensure that you have created a database for development(If you're developing with virtual environment)
- Install Docker and Docker Compose
- Activate virtual environment with `python3 -m venv venv`
- Install application dependencies with `pip install -r requirements.txt`

## Starting the API

> Local Setup

```sh
- $ python manage.py migrate --noinput
- $ python manage.py collectstatic --clear --noinput
- $ python manage.py runserver 8005
```

> Docker and Compose

```sh
# To Start the API
- $ docker-compose up --build

# To Stop the API
- $ docker-compose down
```

The API runs on would run on `http://localhost:8005`

## Testing the API

> Ensure you have a DB running(Using local setup)

```sh
$ pytest -vv
```

## Built With

- [Django](https://www.djangoproject.com/) - Django makes it easier to build better web apps more quickly and with less code.
- [PostgreSQL](https://www.postgresql.org/) - A production-ready relational database system emphasizing extensibility and technical standards compliance.
- [Redis](https://redis.io/) - Redis is an open source (BSD licensed), in-memory data structure store, used as a database, cache, and message broker.
- [Docker](https://www.docker.com/) - Docker is a service products that uses OS-level virtualization to deliver software in packages called containers.

## Author

- **Jesse Egbosionu**
