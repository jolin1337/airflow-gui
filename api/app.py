import inspect
import requests
import json

from flask import Flask, redirect, request
from projects.eloqua.bbm_ces_to_eloqua import dag
from dag_bag_collections import dag_bag, get_operators, filter_operator_arguments
from dag_generator import save_dag
app = Flask(__name__)
operators = get_operators(dag_bag)

@app.route('/')
def index_app_redirect():
    return redirect('http://192.168.0.106:8082/')

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
    dag = dag_bag.dags.get(dag_id)
    dag_file = dag.full_filepath + '.new.py'
    with open(dag_file, 'w') as f:
        save_dag(f, dag, data['graph']['tasks'])
    return dag_graph(dag_id)

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
    url = 'http://192.168.0.106:8085/v1/graphql'
    data = request.data
    req = requests.post(url, data=data)
    print(req.text, req.status_code)
    return req.text, req.status_code


@app.route('/v1/operators')
def get_operators():
    return {
        'operators': list(operators.values())
    }
