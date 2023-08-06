import json
import re

from cquest.confighandle import ConfigHandle
from cquest.utils import data_replace


class Mixins:
    """
    混合调配器
    """

    def __init__(self, configfile=None):
        self.configfile = configfile
        self.all_config_data = self.get_all_config_data()

    # 获取外部配置文件
    # @staticmethod
    # def get_outside_config():
    #     setting_config = ConfigHandle(filenames=SETTING_PATH)
    #     url_relative_path = setting_config.get_value('url', 'path')
    #     url_path = os.path.join(get_ccp_xmind_path(), url_relative_path)
    #     return url_path

    # 顺序获取所有config数据
    def get_all_config_data(self):
        config = ConfigHandle(self.configfile)
        all_config_data = config.get_all_data()
        return all_config_data

    # 根据入参提取所有config数据
    def data_extraction(self, name_list):
        data = {}
        for item in name_list:
            value = self.all_config_data.get(item)
            data.setdefault(item, value)
        return data

    # 替换数据,将特定字符 '${}' 包括引号,全部替换为目标数据
    # @staticmethod
    # def data_replace(source, pattern, current):
    #     """
    #     数据替换
    #     """
    #     if isinstance(current, (dict, list, tuple)):
    #         current = json.dumps(current)
    #         new_source = source.replace('"${%s}"' % pattern, current)
    #         return new_source
    #     elif isinstance(current, str):
    #         new_source = source.replace('${' + pattern + '}', current)
    #         return new_source
    #     elif isinstance(current, int):
    #         new_source = source.replace('${' + pattern + '}', str(current))
    #         return new_source
    #     else:
    #         print(type(current), '替换内容类型不被支持')
    #         return source

    # 数据融合,将第三方数据合并到提取的数据特定字段中
    @staticmethod
    def data_fusion(source, current):
        """
        入参 全局匹配替换变量参数值
        """
        json_data = json.dumps(source)

        _KEYCRE = re.compile(r"\${([^}]+)}")
        findall_item = re.findall(_KEYCRE, json_data)

        if set(current.keys()).intersection(set(findall_item)):
            for pattern in current:
                if pattern in findall_item:
                    json_data = data_replace(json_data, pattern, current.get(pattern))
            new_data = json.loads(json_data)
            return new_data
        else:
            return source

    def data_extraction_fusion(self, name: list, tripartite: dict):
        """
        多数据提取替换,根据入参提取数据并融合三方数据
        """
        data = {}
        for item in name:
            # 提取数据
            value = self.all_config_data.get(item)
            # 融合数据
            if item in tripartite:
                value = self.data_fusion(value, tripartite.get(item))
                data.setdefault(item, value)
        return data
