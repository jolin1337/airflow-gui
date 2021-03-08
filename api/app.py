import inspect
import requests
import json

from flask import Flask, redirect, request
from projects.eloqua.bbm_ces_to_eloqua import dag
from dag_bag_collections import dag_bag, get_operators, filter_operator_arguments
from dag_generator import save_dag, dag_to_dict
app = Flask(__name__)
operators = get_operators(dag_bag)

services = {
    'frontend': 'http://192.168.0.106:8082/',
    'graphql': 'http://192.168.0.106:8085/v1/graphql',
    'airflow': 'http://192.168.0.106:8080/'
}

@app.route('/')
def index_app_redirect():
    return redirect(services['frontend'])

@app.route('/v1/dags/<string:dag_id>/graph')
def dag_graph(dag_id):
    dag = dag_bag.dags.get(dag_id)
    if dag is None:
        print("Dag was not found:", dag_id)
        return {'error': 'Unkown dag id'}, 404
    # TODO: Move to dag_generator module
    resp = {
        'graph': dag_to_dict(dag)
    }
    return resp

@app.route('/v1/dags/<string:dag_id>/graph', methods=['POST'])
def post_save_dag(dag_id):
    data = json.loads(request.data)
    if not data.get('message'):
        return {'error': 'invalid message'}, 400
    dag = dag_bag.dags.get(dag_id)
    dag_file = dag.full_filepath + '.new.py'
    with open(dag_file, 'w') as f:
        save_dag(f, dag, data['graph']['tasks'])
        # TODO: Add save commit and optional save PR in kirby
    return dag_graph(dag_id)

@app.route('/v1/dags/<string:dag_id>/trigger', methods=['POST'])
def post_trigger_dag(dag_id):
    url = services['airflow'] + '/admin/airflow/trigger'
    data = json.loads(request.data)
    query = f'?dag_id={dag_id}&origin=/admin/airflow/tree?dag_id={dag_id}'
    # TODO: Authenticate towards airflow with session (e.q. request services['airflow'] + '/admin' to retrieve session and csrf_token)
    cookies = {
        'session': 'eyJfZnJlc2giOmZhbHNlLCJjc3JmX3Rva2VuIjoiMTRkMTFhOGI0NDBhYzc1NjcwNGRhZWY3YmY1NzE1MjE2MDc4YTJmMSJ9.YEXVnA.gzhUyzAAiK8PJS08eHKGdZ33w6A'
    }
    files = {
        'dag_id': (None, data['dag_id']),
        'conf': (None, data['conf']),
        'csrf_token': (None, 'IjE0ZDExYThiNDQwYWM3NTY3MDRkYWVmN2JmNTcxNTIxNjA3OGEyZjEi.YEXVnA.KGp4b52IPCIDUztxXvK7F5LNtTQ')
    }
    resp = requests.post(url + query, cookies=cookies, files=files)
    return resp.text, resp.status_code

@app.route('/v1/dags/<string:dag_id>/tasks/<string:task_id>')
def task_info(dag_id, task_id):
    dag = dag_bag.dags.get(dag_id)
    if dag is None:
        print("Dag was not found:", dag_id)
        return {'error': 'Unkown dag id'}, 404
    task = dag.task_dict.get(task_id)
    if task is None:
        print("Task was not found:", task_id)
        return {'error': 'Unkown task id'}, 404
    # TODO: Add information about run history etc...
    return {
        'task': {
            'task_id': task_id
        }
    }


@app.route('/v1/graphql', methods=['POST'])
def graphql():
    url = services['graphql']
    data = request.data
    req = requests.post(url, data=data)
    print(req.text, req.status_code)
    return req.text, req.status_code


@app.route('/v1/operators')
def get_operators():
    return {
        'operators': list(operators.values())
    }
