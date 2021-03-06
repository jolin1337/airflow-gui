""" add additional DAGs folders to be used by airflow to check where to look for dag files """
import os
import importlib
import inspect

from airflow.models.baseoperator import BaseOperator
from airflow.models import DagBag

dag_bag = DagBag()


def collect_dags_in_dag_bag(dag_bag):
    current_file_path = os.path.join(os.path.dirname(__file__), 'kirby/scheduled/dags')
    base_path = os.path.join(current_file_path, 'projects')
    dags_dirs = os.listdir(base_path)
    def process_file(file_path):
        # TODO: Use this method istead of dag_bag.process_file
        if __file__.endswith(os.path.basename(file_path)) or not file_path.endswith('.py') or not os.path.isfile(file_path):
            return
        file_path = file_path.replace(current_file_path, '').strip('/')
        module = importlib.import_module(
            file_path[:-len('.py')].replace('/', '.'))
        #for key, data in inspect.getmembers(module, inspect.isclass):
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


def register_base_operator_injection(task_instances):
    class Dummy:
        pass

    def base_init_method(self, *args, **kwargs):
        base_operator_init(self, *args, **kwargs)
        frame = inspect.currentframe()
        frame_locals = frame.f_locals.copy()
        while frame.f_back is not None and isinstance(frame.f_back.f_locals.get('self', Dummy()), BaseOperator):
            frame = frame.f_back
            frame_locals = {
                **frame_locals,
                **frame.f_locals.copy()
            }

        frame_locals.pop('frame')
        frame_locals.pop('self')
        if '__class__' in frame_locals:
            frame_locals.pop('__class__')
        if 'dag' in frame_locals.get('kwargs', {}) and 'dag' in frame_locals['kwargs']:
            frame_locals['kwargs'].pop('dag')
        if 'dag' in kwargs:
            kwargs.pop('dag')
        task_instances[self.dag.dag_id + '_' + self.task_id] = {
            'operator_name': self.task_type,
            'self_locals': frame_locals
        }

    base_operator_init = BaseOperator.__init__
    BaseOperator.__init__ = base_init_method
    return base_init_method

def unregister_base_operator_injection(reset_method):
    BaseOperator.__init__ = reset_method

def get_operators(dag_bag):
    operators = {}
    for dag in dag_bag.dags.values():
        for task in dag.tasks:
            task_type = task.task_type
            operators[task_type] = {}
            operators[task_type]['operator_name'] = task_type
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
                        **arguments.get(param['name'], {}) # First class in classes list should have priority for default values
                    }
            operators[task_type]['arguments'] = list(arguments.values())
    return operators

def get_task_instances(dag_bag):
    task_instances = {}
    reset_method = register_base_operator_injection(task_instances)
    collect_dags_in_dag_bag(dag_bag)

    unregister_base_operator_injection(reset_method)
    return task_instances


def filter_operator_arguments(operator, task_locals):
    arguments = operator['arguments']
    res = {}
    for i, arg in enumerate(arguments):
        if len(task_locals['args']) > i:
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
