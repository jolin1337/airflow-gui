import json
import textwrap
import os
import re
import functools

import git
from dag_bag_collections import get_task_instances, get_operators, filter_operator_arguments, stringify_value
from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import DagBag

operators = get_operators()
task_instances = get_task_instances(operators)

def dag_to_dict(dag: DAG) -> dict:
    key = f'{dag.dag_id}_{dag.tasks[0].task_id}'
    return {
        'dag_id': dag.dag_id,
        'tasks': [
            {
                'task_id': task.task_id,
                'upstream': list(task.upstream_task_ids),
                'downstream': list(task.downstream_task_ids),
                'task_type': task.task_type,
                'arguments': task_instances[f'{dag.dag_id}_{task.task_id}']['arguments'],
            } for task in dag.tasks
        ]
    }

class DagGenerator:
    def __init__(self, dag):
        self.dag = dag
        self.imports = set()
        self.tasks = {}
        self.downstream = {}
        self.variables = set()
    def __add_import(self, what, module=None, alias=None):
        if module is None:
            imp = f'import {what}'
        else:
            imp = f'from {module} import {what}'
        if alias is not None:
            imp += f' as {alias}'
        self.imports.add(imp)

    @property
    def import_string(self):
        return '\n'.join(self.imports)

    @property
    def dag_string(self):
        self.__add_import('DAG', 'airflow')
        return '\n\n' + textwrap.dedent(f'''
            default_args = {stringify_value(self.dag.default_args, imports=self.imports)}

            dag = DAG(
                dag_id='{self.dag.dag_id}',
                schedule_interval='{self.dag.schedule_interval}',
                default_args=default_args,
                description={stringify_value(self.dag.description, imports=self.imports)},
                # https://airflow.apache.org/faq.html#what-s-the-deal-with-start-date
                # start_date=days_ago(1),
                catchup={self.dag.catchup},
                # https://stackoverflow.com/a/63955004 for explanation:
                concurrency={self.dag.concurrency},
                max_active_runs={self.dag.max_active_runs}
            )
            '''[1:])

    @property
    def tasks_string(self):
        return '\n'.join(task for task in self.tasks.values())

    @property
    def dependencies_string(self):
        return '\n'.join(
            self.tasks[taska].split('=')[0] + '>>' + self.tasks[taskb].split('=')[0]
            for taska, deps in self.downstream.items()
            for taskb in deps
        )

    def add_task(self, task):
        operator = operators[task['task_type']]
        self.__add_import(operator['operator_name'],
                          module=operator['operator_module'])
        params = [','.join(task['arguments']['args'])] if task['arguments'].get('args') else []
        for param_name, param in task['arguments'].items():
            if param_name == 'args' or param_name == 'dag': # We have already dealt with these before the loop
                continue
            if param_name == 'kwargs':
                for p, v in param.items():
                    # IF it is a method definition
                    if re.match(r'^def [a-zA-Z]', v) is not None:
                        self.__add_variable(v)
                        # TODO: Test this!!!
                        v = re.sub(r'^def (.*?)\(', '$1', v)
                    elif '\n' in v:
                        v = textwrap.indent(v, '    ' * 4)
                    params.append(f'{p}={v}') # stringify_value(v, indentation=4, imports=self.imports).lstrip()}')
            else:
                if '\n' in param:
                    param = textwrap.indent(param, '    ' * 4)
                param_str = f'{param_name}={param}' # stringify_value(param, indentation=4, imports=self.imports).lstrip()}'
                params.append(param_str)
        param_str = ',\n                '.join(params)
        self.tasks[task['task_id']] = textwrap.dedent(f'''
            task_{len(self.tasks) + 1} = {operator['operator_name']}(
                dag=dag,
                {param_str}
            )
            '''[1:])
        self.downstream[task['task_id']] = task['downstream']

def save_dag(dag: DAG, tasks: list, commit_message=None, create_pr=False) -> None:
    def sort_task(a, b):
        if b['task_id'] in a['upstream']:
            return 1
        elif a['task_id'] in b['upstream']:
            return -1
        return 0
    dag_file = dag.full_filepath + '.new'
    with open(dag_file, 'w') as fh:
        dg = DagGenerator(dag)
        for task in sorted(tasks, key=functools.cmp_to_key(sort_task)):
            dg.add_task(task)
        dag_file_string = f'{dg.dag_string}\n{dg.tasks_string}\n{dg.dependencies_string}'
        fh.write(dg.import_string)
        fh.write(dag_file_string)

    dag_bag = DagBag()
    temp_dag = dag_bag.process_file(dag_file)
    if not temp_dag:
        # os.unlink(dag_file)
        return False
    else:
        os.rename(dag_file, dag.full_filepath)
    if commit_message is not None:
        os.chdir(os.path.dirname(__file__) + '/kirby')
        date = datetime.now()
        git.checkout(f'code-changes-{date:%Y%m%d-%H%M%s}', new=True)
        print(git.status())
        # print(git.diff())
        git.commit(commit_message, add_all=True)
        # git.push()
        # if create_pr:
        #     git.create_pr('Changes from airflow: ' + commit_message)
        # git.checkout('master')
        return True
    return False
