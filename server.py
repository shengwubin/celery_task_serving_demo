from flask import Flask, Response, request, jsonify
from dotenv import load_dotenv
import os
import requests
from worker import add
from worker import app as celery_app
from celery.exceptions import TimeoutError
from celery.result import AsyncResult

load_dotenv(override=False)

CELERY_FLOWER_METRICS_URL = os.getenv('CELERY_FLOWER_METRICS_URL', 'http://localhost:5555/metrics')

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "<p>celery task test</p>"


@app.route("/submit", methods=["POST"])
def submit():
    payload = request.get_json(force=True)
    timeout = payload.get('timeout', 10)
    result = add.delay(*payload['args'])
    try:
        res = result.get(timeout=timeout)
        data = {
            'task_id': result.id,
            'status': 'ready',
            'result': res,
            'msg': 'success'
        }
    except TimeoutError:
        data = {
            'task_id': result.id,
            'result': None,
            'status': 'error',
            'msg': "Task did not finish within 10 seconds."
        }
    except Exception as e:
        data = {
            'task_id': result.id,
            'result': None,
            'status': 'error',
            'msg': str(e)
        }
    return jsonify(data)


@app.route("/asubmit", methods=["POST"])
def asubmit():
    payload = request.get_json(force=True)
    result = add.delay(*payload['args'])
    return {
        'task_id': result.id
    }


@app.route("/check/<task_id>", methods=["GET"])
def check(task_id: str):
    try:
        result = AsyncResult(task_id, app=celery_app)
        if result.ready():
            return jsonify({
                'task_id': task_id,
                'status': 'ready',
                'result': result.get(),
                'msg': 'success'
            })
        else:
            return jsonify({
                'task_id': task_id,
                'status': 'pending',
                'result': None,
                'msg': 'task is not ready'
            })
    except Exception as e:
        return jsonify({
            'task_id': task_id,
            'result': None,
            'status': 'error',
            'msg': str(e)
        })


@app.route('/metrics', methods=['GET'])
def metrics():
    try:
        response = requests.get(CELERY_FLOWER_METRICS_URL)
        # 从原始响应创建一个Flask响应对象
        # 并复制status_code和所有headers
        resp = Response(response.content, status=response.status_code)
        for header_name, header_value in response.headers.items():
            resp.headers[header_name] = header_value
        return resp
    except requests.RequestException as e:
        return f"Error fetching metrics: {e}", 500
