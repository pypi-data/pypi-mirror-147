import json
import re

from jsonpath import jsonpath

from cquest.loggings import logger
from cquest.mixins import Mixins
from cquest.sessions import Sessions
from cquest.utils import data_replace, deal_json_invalid, type_judgment, path_judgment


class Composer(Sessions):
    """
    执行器
    """

    def __init__(self, configfile=None, is_continue=False):
        super().__init__()
        self.configfile = configfile
        self.associated_variable = {}
        self.is_continue = is_continue
        self.hooks = {}
        self.hook_item = {}

    def registers(self, api_name):
        """
        断言注册
        """
        if self.hooks:
            for item in self.hooks:
                if api_name == item:
                    self.hook_item = self.hooks.get(item)

    def generate(self, name, tripartite=None):
        """
        分配数据,与Mixins融合
        """
        title = '未检测到有效的接口配置文件,self.configfile为必填项,请确认入参是否正确'
        configfile = path_judgment(self.configfile, title=title)
        if not configfile:
            return

        mixed = Mixins(configfile)
        if tripartite:
            source_data = mixed.data_extraction_fusion(name, tripartite)
        else:
            source_data = mixed.data_extraction(name)
        for item in source_data.items():
            assertion = item[1].pop('assertion', None)
            associated = item[1].pop('associated', None)
            prepare_request = item[1]
            self.registers(item[0])
            yield prepare_request, assertion, associated

    @staticmethod
    def assertion_log(assertion_data, assertion_result):
        """
        断言日志打印格式封装
        """
        logger.info(f'\n{"-" * 32}[断言数据]{"-" * 32}\n{assertion_data}\n{"-" * 32}[断言结果]{"-" * 32}\n{assertion_result}')

    def assertion_printing(self, check_result=None, assertion_data=None):
        """
        校验结果打印
        """
        if not assertion_data:
            self.assertion_log('无', '无')
            return None
        if 'FAIL' in check_result:
            self.assertion_log(assertion_data, '失败')
            return False
        else:
            self.assertion_log(assertion_data, '成功')
            return True

    # 字典类型断言
    def assertion_dict_type(self, request_result, assertion_data):
        """
        字典类型校验
        """
        check_result = []
        for i, j in assertion_data.items():
            if i in request_result and j == str(request_result[i]):
                check_result.append('PASS')
            else:
                check_result.append('FAIL')
        return self.assertion_printing(check_result, assertion_data)

    def assertion_list_tuple_type(self, request_result, assertion_data):
        """
        列表元组类型断言
        字符串列表类型校验
        """
        check_result = []
        for item in assertion_data:
            if item in request_result:
                check_result.append('PASS')
            else:
                check_result.append('FAIL')
        return self.assertion_printing(check_result, assertion_data)

    def assertion_str_type(self, request_result, assertion_data):
        """
        字符串类型断言
        """
        if assertion_data in request_result:
            result = self.assertion_printing(['PASS'], assertion_data)
        else:
            result = self.assertion_printing(['FAIL'], assertion_data)
        return result

    def assertion(self, request_result, assertion_data):
        """
        断言
        """
        if isinstance(assertion_data, type(request_result)):
            if isinstance(assertion_data, dict):
                return self.assertion_dict_type(request_result, assertion_data)
            elif isinstance(assertion_data, (list, tuple)):
                return self.assertion_list_tuple_type(request_result, assertion_data)
            else:
                return self.assertion_str_type(request_result, assertion_data)
        else:
            return self.assertion_printing(['FAIL'], assertion_data)

    def interpolation(self, params: dict):
        """
        插值
        """
        json_data = json.dumps(params)
        _KEYCRE = re.compile(r"\${([^}]+)}")
        findall_item = re.findall(_KEYCRE, json_data)
        for item in findall_item:
            if item in self.associated_variable:
                json_data = data_replace(json_data, item, self.associated_variable[item])
        params = json.loads(deal_json_invalid(json_data))
        return params

    def dispatch_hook(self, name, hook_data, *args, **kwargs):
        """
        分派钩子
        """
        if self.hook_item:
            if hasattr(self.hook_item, '__call__'):
                self.hook_item = [self.hook_item]
            for hook in self.hook_item:
                if 'response' == name == hook:
                    hook_data.update({'hooks': {'response': self.hook_item.get(hook)}})
                elif name == hook:
                    hook = self.hook_item.get(hook)
                    _hook_data = hook(hook_data, *args, **kwargs)
                    if _hook_data is not None:
                        hook_data = _hook_data
        return hook_data

    def before_request(self, data_request):
        """
        请求前数据处理
        """
        # 分派钩子
        data_request = self.dispatch_hook('request', data_request)
        data_request = self.dispatch_hook('response', data_request)
        params_list = ['cookies', 'data', 'params']
        for params_item in params_list:
            if params_item in data_request:
                params_obj = data_request.get(params_item)
                params_obj = self.interpolation(params_obj)
                data_request[params_item] = params_obj
        return data_request

    @staticmethod
    def associated_log(associated_data, associated_result):
        """
        关联数据日志打印格式封装
        """
        logger.info(f'\n{"-" * 32}[关联预设]{"-" * 32}\n{associated_data}\n{"-" * 32}[关联数据]{"-" * 32}\n{associated_result}')

    def associated(self, request_result: dict, associated_data: dict):
        """
        关联变量:当前请求中获得结果提供给下一请求调用
        """
        # 关联局部变量
        associated_result = {}
        fail_variable = []
        try:
            for key in associated_data:
                value = associated_data[key]
                jsonpath_result = jsonpath(request_result, value)
                if jsonpath_result:
                    associated_result.update({key: jsonpath_result[0]})
                else:
                    fail_variable.append(value)
            self.associated_variable.update(associated_result)
            self.associated_log(associated_data, associated_result)
            if fail_variable:
                split_line = '-' * 32
                logger.warn(f'\n以下字段无法获得关联数据:{fail_variable}\n{split_line}')
        except TypeError as te:
            logger.debug(f'入参不是字典类型:{te}')
        return associated_result

    def after_request(self, request_result, assertion, associated):
        """
        获得请求出参后校验和关联数据
        """
        assertion = self.dispatch_hook('assertion', assertion)
        if assertion:
            # 分派断言钩子
            assert_result = self.assertion(request_result, assertion)
        else:
            assert_result = self.assertion_printing()

        associated = self.dispatch_hook('associated', associated)
        if associated:
            self.associated(request_result, associated)
        else:
            self.associated_log('无', '无')
        # 同时返回断言结果和请求结果,方便调用方判断和使用结果
        return assert_result, request_result

    @staticmethod
    def body_parse(res):
        if type_judgment(res.text) in [dict, list]:
            res_value = res.json()
        else:
            res_value = res.text
        return res_value

    def request(self, prepare_request, assertion, associated, **kwargs):
        """
        数据请求
        """
        # 请求前
        prepare_request = self.before_request(prepare_request)
        # 发起请求
        res = self.send(prepare_request, **kwargs)
        # 请求结果
        if res:
            res_body = self.body_parse(res)
        else:
            # 请求结果失败的话,同时返回断言和结果都失败
            return False, False
        # 请求后
        assert_result = self.after_request(res_body, assertion, associated)
        return assert_result

    def main(self, names, tripartite=None, hooks=None, **kwargs):
        """
        数据解析,数据集散调度
        """
        logger.debug('\n' + '/' * 32 + ' start' + str(names) + ' ' + '/' * 32)
        self.hooks = hooks or {}
        data_obj = self.generate(names, tripartite=tripartite)
        response_obj = False
        while True:
            try:
                prepare_request, assertion, associated = next(data_obj)
                response_obj = self.request(prepare_request, assertion, associated, **kwargs)
                if not self.is_continue and response_obj[0] is False:
                    logger.warn(f'\n{"-" * 32}[终止执行]{"-" * 32} \n校验失败,停止后续请求!')
                    break
                else:
                    continue
            except StopIteration:
                logger.debug('\n' + '/' * 32 + ' end' + str(names) + ' ' + '/' * 32)
                break
        return response_obj
