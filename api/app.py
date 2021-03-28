import inspect
import json
import os
import pendulum

import requests
from flask import Flask, redirect, request

from log import logger

from dag_bag_collections import (filter_operator_arguments, get_dags,
                                 get_operators)
from dag_generator import dag_to_dict, save_dag
operators = get_operators()
dag_bag = get_dags()

services = {
    'frontend': 'http://192.168.0.106:8082/',
    'graphql': 'http://192.168.0.106:8085/v1/graphql',
    'airflow': 'http://192.168.0.106:8080/'
}


app = Flask(__name__)


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
    if dag and save_dag(dag, data['graph']['tasks'], commit_message=data['message'], create_pr=data.get('create_pr')):
        return dag_graph(dag_id)
    else:
        return {'error': 'Unable to save dag'}, 400


@app.route('/v1/dags/<string:dag_id>/trigger', methods=['POST'])
def post_trigger_dag(dag_id):
    dag = dag_bag.dags.get(dag_id)
    if dag is None:
        print("Dag was not found:", dag_id)
        return {'error': 'Unkown dag id'}, 404
    print("running dag")
    now = pendulum.now()
    # Runs dag inplace
    #print("RUN dag", dag.run(start_date=now, end_date=now))
    print("create dagrun", dag.create_dagrun(f'airflow_gui_{now}', start_date=now, execution_date=now, external_trigger=True, state=None))


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


@app.route('/v1/dags/<string:dag_id>/tasks/<string:task_id>/logs')
def get_task_log(dag_id, task_id):
    dag = dag_bag.dags.get(dag_id)
    if dag is None:
        print("Dag was not found:", dag_id)
        return {'error': 'Unkown dag id'}, 404
    task = dag.task_dict.get(task_id)
    if task is None:
        print("Task was not found:", task_id)
        return {'error': 'Unkown task id'}, 404
    data = {
        **dict(request.args),
        'dag_id': dag_id,
        'task_id': task_id
    }
    print(data)
    resp = requests.get(services['airflow'] + '/admin/airflow/get_logs_with_metadata', params=data)
    return resp.text, resp.status_code

@app.route('/v1/graphql', methods=['POST'])
def graphql():
    url = services['graphql']
    data = request.data
    req = requests.post(url, data=data)
    return req.text, req.status_code


@app.route('/v1/operators')
def get_operators():
    return {
        'operators': list(operators.values())
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
