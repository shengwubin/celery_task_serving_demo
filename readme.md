# celery_task_serving_demo

This is only a demo for celery task serving. It includes:

1. Celery worker
2. Flower for monitoring
3. A simple flask server to submit and monitor tasks
4. Dockerfile and docker-compose.yml
5. Redis for broker and PostgreSQL for result backend

## Run without docker

### Install broker dependencies

Install redis on your local machine, and the default configuration is `redis://localhost:6379/0`:

### Add a `.env` file to the root directory

Example:

```shell
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
CELERY_FLOWER_METRICS_URL=http://localhost:5555/metrics
```

### Install dependencies

```shell
pip install -r requirements.txt
```

### Run celery worker

```shell
celery -A worker.app worker --loglevel=INFO
```

### Run flower

```shell
celery -A worker.app --broker=redis://redis:6379/0 --result-backend=redis://redis:6379/0
```

You can visit `http://localhost:5555` to monitor the celery worker.

### Start flask server

```shell
FLASK_APP=server flask run
```

Your flask server will run on `http://localhost:5000`.

### Submit a task and get the result immediately

```shell
curl --location 'http://127.0.0.1:5000/submit' \
--header 'Content-Type: application/json' \
--data '{
    "timeout": 10,
    "args": [
        4,
        4
    ]
}'
```

### Submit a task and the task if

```shell
curl --location 'http://127.0.0.1:5000/asubmit' \
--header 'Content-Type: application/json' \
--data '{
    "args": [
        4,
        4
    ]
}'
```

### Get the result of a task

```shell
curl --location 'http://127.0.0.1:5000/check/{your-id-from-previous-submit}'
```

### Get the metrics of celery worker from flower

```shell
curl --location 'http://127.0.0.1:5000/metrics'
```

## Run with docker

### Build

```shell
docker build -t celery_task_serving_demo:latest .
```

### Run

```shell
docker-compose up
```

### Run in background

```shell
docker-compose up -d
```
