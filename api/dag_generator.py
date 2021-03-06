import textwrap
from dag_bag_collections import dag_bag, get_task_instances, get_operators, filter_operator_arguments
from airflow import DAG

task_instances = get_task_instances(dag_bag)
operators = get_operators(dag_bag)

def dag_to_dict(dag: DAG) -> dict:
    return {
        'dag_id': dag_id,
        'tasks': [
            {
                'task_id': task.task_id,
                'upstream': list(task.upstream_task_ids),
                'downstream': list(task.downstream_task_ids),
                'task_type': task.task_type,
                'arguments': filter_operator_arguments(operators[task.task_type], task_instances[dag_id + '_' + task.task_id]['self_locals']),
            } for task in dag.tasks
        ]
    }

class DagGenerator:
    def __init__(self, dag):
        self.imports = []
        self.tasks = []
    def __add_import(self, what, module=None, alias=None):
        if module is None:
            imp = f'import {what}'
        else:
            imp = f'from {module} import {what}'
        if alias is not None:
            imp += f' as {alias}'
        self.imports.append(imp)

    @property
    def import_string(self):
        return '\n'.join(self.imports)

    @property
    def dag_string(self):
        return textwrap.dedent(f'''
            default_args = {dag.default_args}

            dag = Dag(
                dag_id='{dag.dag_id}',
                schedule_interval='{dag.schedule_interval}',
                default_args=default_args,
                description='{dag.description}',
                # https://airflow.apache.org/faq.html#what-s-the-deal-with-start-date
                # start_date=days_ago(1),
                catchup=False,
                # https://stackoverflow.com/a/63955004 for explanation:
                concurrency=3,
                max_active_runs=10
            )
        ''')
    def __add_task(self, task):


def save_dag(fh, dag: DAG, tasks: list) -> None:
    dag_def = f'''
    from airflow import DAG
    from airflow.contrib.operators import bigquery_operator
    from airflow.operators.latest_only_operator import LatestOnlyOperator

    default_args = {dag.default_args}

    dag = Dag(
        dag_id='{dag.dag_id}',
        schedule_interval='{dag.schedule_interval}',
        default_args=default_args,
        description='{dag.description}',
        # https://airflow.apache.org/faq.html#what-s-the-deal-with-start-date
        # start_date=days_ago(1),
        catchup=False,
        # https://stackoverflow.com/a/63955004 for explanation:
        concurrency=3,
        max_active_runs=10
    )
    '''
    fh.write(dag_def)
