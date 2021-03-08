import json
import textwrap
import re

from dag_bag_collections import dag_bag, get_task_instances, get_operators, filter_operator_arguments
from datetime import datetime, timedelta
from airflow import DAG

task_instances = get_task_instances(dag_bag)
operators = get_operators(dag_bag)

def dag_to_dict(dag: DAG) -> dict:
    return {
        'dag_id': dag.dag_id,
        'tasks': [
            {
                'task_id': task.task_id,
                'upstream': list(task.upstream_task_ids),
                'downstream': list(task.downstream_task_ids),
                'task_type': task.task_type,
                'arguments': filter_operator_arguments(operators[task.task_type], task_instances[dag.dag_id + '_' + task.task_id]['self_locals']),
            } for task in dag.tasks
        ]
    }

class DagGenerator:
    def __init__(self, dag):
        self.dag = dag
        self.imports = []
        self.tasks = {}
        self.downstream = {}
    def __add_import(self, what, module=None, alias=None):
        if module is None:
            imp = f'import {what}'
        else:
            imp = f'from {module} import {what}'
        if alias is not None:
            imp += f' as {alias}'
        if imp not in self.imports:
            self.imports.append(imp)

    @property
    def import_string(self):
        return '\n'.join(self.imports)

    @property
    def dag_string(self):
        self.__add_import('DAG', 'airflow')
        return '\n\n' + textwrap.dedent(f'''
            default_args = {self.__stringify_value(self.dag.default_args)}

            dag = DAG(
                dag_id='{self.dag.dag_id}',
                schedule_interval='{self.dag.schedule_interval}',
                default_args=default_args,
                description={self.__stringify_value(self.dag.description)},
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

    def __stringify_value(self, value, indentation=0):
        if isinstance(value, datetime):
            self.__add_import('datetime')
            return f'datetime.datetime({value.year}, {value.month}, {value.day}, {value.hour}, {value.minute}, {value.second})'
        if isinstance(value, timedelta):
            self.__add_import('datetime')
            return f'datetime.timedelta(days={value.days}, seconds={value.seconds})'
        if isinstance(value, bool) or isinstance(value, int) or isinstance(value, float):
            return f'{value}'
        if isinstance(value, str) and '\n' in value:
            return textwrap.indent(f'\'\'\'{value}\'\'\'', '    ' * indentation)
        if isinstance(value, str):
            return f'\'{value}\''
        if isinstance(value, dict):
            value_str = '{'
            for k, v in value.items():
                value_str += f'"{k}": {self.__stringify_value(v)}, '
            value_str = value_str[:-2] + '}'
            return value_str
        if isinstance(value, list):
            value_str = '[  '
            for v in value:
                value_str += f'{self.__stringify_value(v)}, '
            value_str = value_str[:-2] + ']'
            return value_str
        return f'{value}'

    def add_task(self, task):
        operator = operators[task['task_type']]
        self.__add_import(operator['operator_name'],
                          module=operator['operator_module'])
        params = [','.join(task['arguments']['args'])] if task['arguments'].get('args') else []
        for param_name, param in task['arguments'].items():
            if param_name == 'args':
                continue
            #if isinstance(param, dict):
            if param_name == 'kwargs':
                for p, v in param.items():
                    params.append(f'{p}={self.__stringify_value(v, 4).lstrip()}')
            else:
                param_str = f'{param_name}={self.__stringify_value(param, 4).lstrip()}'
                params.append(param_str)
        param_str = ',\n                '.join(params)
        self.tasks[task['task_id']] = textwrap.dedent(f'''
            task_{len(self.tasks) + 1} = {operator['operator_name']}(
                {param_str}
            )
            '''[1:])
        self.downstream[task['task_id']] = task['downstream']

def save_dag(fh, dag: DAG, tasks: list) -> None:
    dg = DagGenerator(dag)
    for task in tasks:
        dg.add_task(task)
    fh.write(dg.import_string)
    fh.write(dg.dag_string)
    fh.write(dg.tasks_string)
    fh.write(dg.dependencies_string)
    print("YEYEYEYE")
