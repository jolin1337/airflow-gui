""" add additional DAGs folders to be used by airflow to check where to look for dag files """
import os
import json
import importlib
import textwrap
import inspect
from datetime import datetime, timedelta

from airflow.models.baseoperator import BaseOperator
from airflow.models import DagBag

dag_bag = DagBag()


def __add_import(what, imports, module=None, alias=None):
    if imports is None:
        return
    if module is None:
        imp = f'import {what}'
    else:
        imp = f'from {module} import {what}'
    if alias is not None:
        imp += f' as {alias}'
    imports.add(imp)


def stringify_value(value, indentation=0, imports=None):
    if value is None:
        return 'None'
    if isinstance(value, datetime):
        __add_import('datetime', imports)
        return f'datetime.datetime({value.year}, {value.month}, {value.day}, {value.hour}, {value.minute}, {value.second})'
    if isinstance(value, timedelta):
        __add_import('datetime', imports)
        return f'datetime.timedelta(days={value.days}, seconds={value.seconds})'
    if isinstance(value, bool) or isinstance(value, int) or isinstance(value, float):
        return f'{value}'
    if isinstance(value, str) and '\n' in value:
        return textwrap.indent(f'\'\'\'{value}\'\'\'', '    ' * indentation)
    if isinstance(value, str):
        return json.dumps(value)  # f'\'{value}\''
    if isinstance(value, dict):
        value_str = '{  '
        for k, v in value.items():
            value_str += f'"{k}": {stringify_value(v, indentation, imports)}, '
        value_str = value_str[:-2] + '}'
        return value_str
    if isinstance(value, list):
        value_str = '[  '
        for v in value:
            value_str += f'{stringify_value(v, indentation, imports)}, '
        value_str = value_str[:-2] + ']'
        return value_str
    if callable(value):
        return inspect.getsource(value)
    return f'{value}'


def collect_dags_in_dag_bag(dag_bag):
    current_file_path = os.path.join(
        os.path.dirname(__file__), 'kirby/scheduled/dags')
    base_path = os.path.join(current_file_path, 'projects')
    dags_dirs = os.listdir(base_path)

    def process_file(file_path):
        # TODO: Use this method istead of dag_bag.process_file
        if __file__.endswith(os.path.basename(file_path)) or not file_path.endswith('.py') or not os.path.isfile(file_path):
            return
        file_path = file_path.replace(current_file_path, '').strip('/')
        module = importlib.import_module(
            file_path[:-len('.py')].replace('/', '.'))
        # for key, data in inspect.getmembers(module, inspect.isclass):
        # dag_bag.process_file(os.path.join(, f))

    for f in os.listdir(current_file_path):
        if __file__.endswith(f) or not f.endswith('.py'):
            continue
        dag_bag.process_file(os.path.join(current_file_path, f))

    for d in dags_dirs:
        folder_path = os.path.join(base_path, d)
        if not os.path.isdir(folder_path):
            continue
        dags_files = os.listdir(folder_path)
        for f in dags_files:
            if f.endswith('.py'):
                dag_bag.process_file(os.path.join(base_path, d, f))
    for dag_id, dag in dag_bag.dags.items():
        globals()[dag_id] = dag


def get_operators():
    temp_dagbag = DagBag()
    collect_dags_in_dag_bag(temp_dagbag)
    operators = {}
    for dag in temp_dagbag.dags.values():
        for task in dag.tasks:
            task_type = task.task_type
            operators[task_type] = {}
            operators[task_type]['operator_name'] = task_type
            operators[task_type]['operator_module'] = task.__module__
            operators[task_type]['operator_about'] = task.__doc__
            arguments = {}
            classes = [task.__class__]
            super_classes = list(task.__class__.__bases__)
            while super_classes:
                current_class = super_classes.pop()
                if issubclass(current_class, BaseOperator) or current_class == BaseOperator:
                    classes.append(current_class)
                    super_classes += list(current_class.__bases__)
            for task_class in classes:
                for parameter in inspect.signature(task_class.__init__).parameters.values():
                    if parameter.name == 'self':
                        continue
                    formated_param = inspect.formatargspec([parameter])[
                        1:-1].split(':')
                    param = {}
                    param['name'] = parameter.name
                    if len(formated_param) > 1:
                        annotations = formated_param[1].split('=')
                        param['data_type'] = annotations[0]
                        if len(annotations) > 1:
                            param['default'] = annotations[1]
                    elif '=' in formated_param[0]:
                        annotations = formated_param[0].split('=')
                        param['default'] = annotations[1]
                    arguments[param['name']] = {
                        **param,
                        # First class in classes list should have priority for default values
                        **arguments.get(param['name'], {})
                    }
            operators[task_type]['arguments'] = list(arguments.values())
    return operators


def __override_operators(operators, task_instances):
    def constructor_override(op_name, op_init):
        def constructor_override(self, *args, **kwargs):
            # task_type = type(self).__name__
            op_init(self, *args, **kwargs)
            task_id = kwargs.get('task_id')
            dag_id = kwargs.get('dag').dag_id
            task_instances[f'{dag_id}_{task_id}'] = {
                'operator_name': op_name,
                'arguments': {k: stringify_value(v) for k, v in kwargs.items()}
            }
        return constructor_override

    op_resets = {}
    for op in operators.values():
        op_module = importlib.import_module(op['operator_module'])
        op_class = getattr(op_module, op['operator_name'])
        op_resets[op['operator_name'] +
                  op['operator_module']] = op_class.__init__
        op_class.__init__ = constructor_override(
            op['operator_name'], op_class.__init__)
    return op_resets


def __reset_operators(operators, resets):
    for op in operators.values():
        op_module = importlib.import_module(op['operator_module'])
        op_class = getattr(op_module, op['operator_name'])
        op_class.__init__ = resets[op['operator_name'] + op['operator_module']]


def get_task_instances(operators):
    task_instances = {}
    resets = __override_operators(operators, task_instances)
    temp_dagbag = DagBag()
    collect_dags_in_dag_bag(temp_dagbag)
    # for dag in temp_dagbag.dags.values():
    #     for task in dag.tasks:
    #         arguments = filter_operator_arguments(operators[task.task_type], task)
    #         task_instances[f'{dag.dag_id}_{task.task_id}'] = {
    #             'operator_name': task.task_type,
    #             'arguments': arguments
    #         }
    __reset_operators(operators, resets)
    return task_instances


def get_dags():
    temp_dagbag = DagBag()
    collect_dags_in_dag_bag(temp_dagbag)
    return temp_dagbag


def filter_operator_arguments(operator, self):
    '''
    OBS: This method assumes that we assign the parameters to self!
    '''
    arguments = operator['arguments']
    res = {}
    for i, arg in enumerate(arguments):
        res[arg['name']] = {
            'name': arg['name'],
            'value': stringify_value(getattr(self, arg['name'])),
            'default': arg.get('default') or '"None"'
        }
    return res


def filter_operator_arguments2(operator, task_locals):
    arguments = operator['arguments']
    res = {}
    for i, arg in enumerate(arguments):
        if len(task_locals.get('args', [])) > i:
            res[arg] = task_locals['args'][i]
        elif task_locals['kwargs'].get(arg['name']) is not None:
            res[arg['name']] = task_locals['kwargs'][arg['name']]
        elif task_locals.get(arg['name']) is not None and arg['name'] not in ['args', 'kwargs']:
            res[arg['name']] = task_locals[arg['name']]
        elif arg['name'] == 'kwargs' and 'kwargs' in task_locals:
            res[arg['name']] = task_locals['kwargs']
            # for param, value in task_locals['kwargs'].items():
            #     res[param] = value
    return res
