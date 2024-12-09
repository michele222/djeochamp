# Djeochamp

Djeochamp is a simulator of championship that uses real country data (population, area, GDP etc.) as parameters to determine winners in simulated head to head matches, until a winner is determined. Djeochamp is implemented in Python with support of Django and PostgreSQL.

![Djeochamp](djeochamp.jpg?raw=true)

## Install
Clone the repository and make sure you have Docker installed and running.

You can use the following commands to start the server instance and initialize the DB with default data.
```
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py loaddata db.json
```
By default, the instance is accessible at http://127.0.0.1:8000.

You will need to register and login in order to create games.

## Usage

When already installed, you can start the server instance with the following command:
```
docker compose up -d
```
and you can stop the server instance with the following command:
```
docker compose down
```
