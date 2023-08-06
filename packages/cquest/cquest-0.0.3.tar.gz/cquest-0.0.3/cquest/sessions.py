import json

from requests import Request, Session
from requests.adapters import HTTPAdapter
from requests.structures import CaseInsensitiveDict
from urllib3 import Retry

from cquest.loggings import logger
from cquest.utils import type_judgment


class Sessions:
    def __init__(self):
        self.session = Session()
        self.proxies = None

    @staticmethod
    def str_to_dict(data):
        if isinstance(data, str) and data.startswith('{') and data.endswith('}'):
            new_data = eval(data)
            return new_data
        else:
            return data

    def to_dict(self, data):
        """
        将字典的字符串值转换为字典
        :param data: 待处理的字典,嵌套字典的值可能是字符串
        :return: new_dict经过处理后的字典,key为data,若值为字符串,保留数据,
        若值为字典,则转换为json字符串,其他嵌套的字符串字典转换为字典
        """
        new_dict = {}
        for item in data.items():
            if item[0] == "data" and isinstance(item[1], str):
                new_dict.update({item[0]: item[1]})
            elif item[0] == "data" and isinstance(item[1], dict):
                new_data_value = json.dumps(item[1])
                new_dict.update({item[0]: new_data_value})
            else:
                new_value = self.str_to_dict(item[1])
                new_dict.update({item[0]: new_value})
        return new_dict

    def prepare(self, metadata):
        parse_data = self.to_dict(metadata)
        req = Request(**parse_data)
        prepped = self.session.prepare_request(req)
        return prepped

    @staticmethod
    def to_json(data):
        if isinstance(data, CaseInsensitiveDict):
            value = json.dumps(dict(data))
        elif isinstance(data, dict):
            value = json.dumps(data)
        elif data is None:
            value = '无'
        else:
            value = data
        return value

    def req_log(self, req):
        req_data = f'\n{"-" * 32}[请求参数]{"-" * 32}'
        req_keys = ['method', 'url', 'headers', '_cookies', 'body', 'hooks']
        for key_item in req_keys:
            req_value = req.__dict__.get(key_item)
            if key_item in ['headers', 'body']:
                req_value = self.to_json(req_value)
            elif key_item == '_cookies':
                key_item = 'cookies'
            elif key_item in ["hooks"]:
                req_value = json.dumps([f_item.__name__ for f_item in req_value.get('response')])
            req_data += f'\n{key_item}: {req_value}'
        logger.debug(req_data)

    @staticmethod
    def body_to_json(res):
        if type_judgment(res.text) in [dict, list]:
            res_value = json.dumps(res.json(), ensure_ascii=False)
        else:
            res_value = res.text
        return res_value

    def res_log(self, res):
        res_data = f'\n{"-" * 32}[返回参数]{"-" * 32}'
        res_keys = ['status_code', 'headers', 'cookies', 'body']
        for key_item in res_keys:
            res_value = res.__dict__.get(key_item)
            if key_item in ['headers']:
                res_value = self.to_json(res_value)
            elif key_item in ['body']:
                res_value = self.body_to_json(res)
            res_data += f'\n{key_item}: {res_value}'
        logger.debug(res_data)

    def kwargs_handle(self, **kwargs):
        """
        对kwargs中相关字段进行处理
        """
        ignore_data = ('verify', False)
        kwargs = dict(**kwargs)
        if ignore_data in kwargs.items():
            import urllib3
            urllib3.disable_warnings()
        if 'proxies' not in kwargs and self.proxies:
            kwargs['proxies'] = self.proxies
        return kwargs

    def send(self, metadata, **kwargs):
        prepped = self.prepare(metadata)
        self.req_log(prepped)
        try:
            kwargs = self.kwargs_handle(**kwargs)
            retry = Retry(connect=3, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            self.session.mount('http://', adapter)
            self.session.mount('https://', adapter)
            res = self.session.send(prepped, **kwargs)
            self.res_log(res)
            return res
        except Exception as e:
            logger.error(f'\n请求异常: {e}')
            return False
