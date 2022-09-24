import json
import os
import platform
import importlib
import sys
from typing import Union, Iterable

import pydantic

from iot.models import FunctionDeviceModel, UniverseNoticeModel


def get_slash():
    if platform.system().lower() == 'windows':
        return '\\'
    else:
        return '/'


def raw_to_function_device_model(message: str) -> FunctionDeviceModel:
    return FunctionDeviceModel(is_raw=True, acoustics='', data=message)


def load_models(path: str):
    importlib.import_module(name=path)


def get_root_path():
    return os.path.dirname(os.path.abspath(__file__))


def get_all_core_packages():
    """
    过于恶心的逻辑，以后优化
    :return:
    """
    g_dirs = list()

    def inner_recursive(path):
        dirs = os.listdir(path)
        for file in dirs:
            new_file = os.path.join(path, file)
            if os.path.isdir(new_file):
                inner_recursive(new_file)
            else:
                g_dirs.append(new_file)
        return g_dirs

    file_abs_paths = inner_recursive(os.path.dirname(os.path.abspath(__file__)) + get_slash() + 'core')
    result = [file_abs_path[:-3]
              for file_abs_path in file_abs_paths
              if file_abs_path.endswith('.py') and not file_abs_path.endswith('__init__.py')]
    return ['iot' + '.'.join(res.split('iot')[-1].split(get_slash())) for res in result]


def process_bar(num, total, text):
    rate = float(num) / total
    ratenum = int(100 * rate)
    r = '\r' + text + '[{}{}]{}%'.format('*' * ratenum, ' ' * (100 - ratenum), ratenum)
    sys.stdout.write(r)
    sys.stdout.flush()


def mkdir(path: str, dirs: Union[str, Iterable]):
    if isinstance(dirs, str):
        dirs = [dirs]
    for dir in dirs:
        if not os.path.exists(path + get_slash() + dir):
            os.makedirs(path + get_slash() + dir)
