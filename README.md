# stores-api

Stores REST API | Flask

# Project init

```
docker-compose build
docker-compose run --rm app sh -c "flask db init"
```

# How to start local development

```
docker-compose up
```

API Documentation [http://localhost:8000/docs](http://localhost:8000/docs)

# How to run lint

```
docker-compose run --rm app sh -c "flake8"
```
