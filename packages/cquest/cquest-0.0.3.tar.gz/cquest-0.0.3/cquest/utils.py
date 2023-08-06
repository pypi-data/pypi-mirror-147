import json
import os.path
import pathlib
import time
import functools

from cquest.loggings import logger


# 获取cquest项目路径
def base_dir():
    return os.path.dirname(os.path.abspath(__file__))


def get_ccp_xmind_path():
    ccp_xmind_path = os.environ.get('cquest')
    return ccp_xmind_path


def type_conversion(data):
    if isinstance(data, str) and (
            data.startswith('{') and data.endswith('}') or data.startswith('[') and data.endswith(']')):
        return json.loads(data)
    else:
        return data


# 类型判断
def type_judgment(data):
    if isinstance(data, str) and (data.startswith('{') and data.endswith('}')):
        return type(dict())
    elif isinstance(data, str) and (data.startswith('[') and data.endswith(']')):
        return type(list())
    elif isinstance(data, str) and (data.startswith('(') and data.endswith(')')):
        return type(tuple())
    else:
        return type(data)


def path_judgment(path, **kwargs):
    try:
        if path:
            path_obj = pathlib.Path(path)
            path_result = path_obj.exists()
            if path_result:
                return path
            else:
                title = '路径不存在'
                if 'title' in kwargs:
                    title = kwargs.get('title')
                raise FileExistsError(f'{path}{title}')
        else:
            title = '路径不存在'
            if 'title' in kwargs:
                title = kwargs.get('title')
            raise FileExistsError(f'{path}{title}')
    except FileExistsError as f:
        logger.error(f'\n{repr(f)}')


# 指定名称和类型的文件判断
def file_judgment(path, file):
    file_path = os.path.join(path, file)
    title = '文件不存在'
    path = path_judgment(file_path, title=title)
    return path


# 11位-当前时间戳
def timestamp(definition='ms'):
    """
    definition=13位毫秒ms & 16位微秒us
    :return:
    """
    try:
        t = time.time()
        if definition == 'ms':
            return int(round(t * 1000))  # 毫秒级时间戳
        elif definition == 'us':
            return int(round(t * 1000000))  # 微秒级时间戳
        else:
            raise ValueError('只允许填写毫秒"ms"和微秒"us"')
    except ValueError as v:
        logger.error(f'抛出异常:{repr(v)}')


# 替换数据,将特定字符 '${}' 包括引号,全部替换为目标数据
def data_replace(source, pattern, current):
    if isinstance(current, (dict, list, tuple)):
        current = json.dumps(current)
        new_source = source.replace('"${%s}"' % pattern, current)
        return new_source
    elif isinstance(current, str):
        new_source = source.replace('${' + pattern + '}', current)
        return new_source
    elif isinstance(current, int):
        new_source = source.replace('${' + pattern + '}', str(current))
        return new_source
    else:
        print(type(current), '替换内容类型不被支持')
        return source


# json兼容换行符和引号
def deal_json_invalid(data: str):
    data = data \
        .replace('\n', '\\n') \
        .replace('\r', '\\r') \
        .replace('\n\r', '\\n\\r') \
        .replace('\r\n', '\\r\\n') \
        .replace('\t', '\\t')

    data = data \
        .replace('": "', '~~jsonSwap~~') \
        .replace('", "', '!!jsonSwap!!') \
        .replace('{"', '@@jsonSwap##') \
        .replace('"}', '$$jsonSwap$$') \
        .replace('], "', '%%jsonSwap%%') \
        .replace('": ', '^^jsonSwap^^') \
        .replace(', "', '&&jsonSwap&&') \
        .replace('None, "', '**jsonSwap**')

    data = data \
        .replace('~~jsonSwap~~', '": "') \
        .replace('!!jsonSwap!!', '", "') \
        .replace('@@jsonSwap##', '{"') \
        .replace('$$jsonSwap$$', '"}') \
        .replace('%%jsonSwap%%', '], "', ) \
        .replace('^^jsonSwap^^', '": ', ) \
        .replace('&&jsonSwap&&', ', "', ) \
        .replace('**jsonSwap**', 'None, "', )

    return data


# 循环函数装饰器
def func_loop(num: int):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            flag = 0
            while flag < num:
                flag += 1
                func(*args, **kwargs)

        return wrapper

    return decorator
