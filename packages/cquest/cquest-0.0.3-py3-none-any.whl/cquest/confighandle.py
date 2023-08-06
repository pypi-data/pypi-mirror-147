import json
from configparser import ConfigParser, ExtendedInterpolation

import chardet as chardet


class ConfigHandle:  # 新建config类

    def __init__(self, filenames=None):
        self.filenames = filenames
        f = open(self.filenames, 'rb')  # 先用二进制打开
        data = f.read()  # 读取文件内容
        encoding = chardet.detect(data).get('encoding')  # 得到文件的编码格式
        self.config_parser = ConfigParser(interpolation=ExtendedInterpolation())
        self.config_parser.read(self.filenames, encoding=encoding)  # 读取指定配置文件

    def get_value(self, section, option):
        return self.config_parser.get(section, option)

    def get_int(self, section, option):
        return self.config_parser.getint(section, option)

    def get_float(self, section, option):
        return self.config_parser.getfloat(section, option)

    def get_boolean(self, section, option):
        return self.config_parser.getboolean(section, option)

    def get_eval_data(self, section, option):
        return eval(self.get_value(section, option))

    def get_sections(self):
        return self.config_parser.sections()

    def get_options(self, section):
        return self.config_parser.options(section)

    def get_items(self, section):
        return self.config_parser.items(section)

    def get_all_data(self):
        """
        获取配置文件的所有信息,类型为字典
        :return:
        """
        sections = self.get_sections()
        all_data = {}
        for section in sections:
            items = self.get_items(section)
            dict_items = {}
            for option, value in items:
                dict_items.setdefault(option, self.conversion_type(value))
            all_data.setdefault(section, dict_items)
        return all_data

    @staticmethod
    def conversion_type(data):
        if isinstance(data, str) and (data.startswith('{') and data.endswith('}')):
            return json.loads(data)
        elif isinstance(data, str) and data.startswith('[') and data.endswith(']'):
            return eval(data)
        else:
            return data

    def to_write(self, section, option, value):
        if section not in self.config_parser.sections():
            self.config_parser.add_section(section)
        self.config_parser.set(section, option, value)

        with open(self.filenames, 'w', encoding='utf-8') as fp:
            self.config_parser.write(fp)

    def remove_option(self, section, option):
        return self.config_parser.remove_option(section, option)


if __name__ == '__main__':
    config = ConfigHandle('../config/url.conf')
    base_value = config.get_value('saveCaseAndScene', 'data')
    print(base_value)
