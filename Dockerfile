# python celery project
FROM python:3.9

RUN apt update && apt install vim tmux git -y
RUN mkdir -p /workspace/celery_task_serving_demo
WORKDIR /workspace/celery_task_serving_demo
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . /workspace/celery_task_serving_demo

