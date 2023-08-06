import os.path

from cquest import root_dir
from cquest.composer import Composer
from cquest.utils import func_loop, timestamp


class Api(Composer):
    """
    用户使用该请求库的主要入口
    配置url.conf后,使用一个类继承Composer进行发起请求
    """

    def __init__(self):
        super(Api, self).__init__()
        # self.proxies为设置全局代理,局部代理可以在main方法中直接赋值,不可使用self.proxies值
        # self.proxies = {
        #     "http": "http://localhost:8888",
        #     "https": "http://localhost:8888",
        # }
        self.configfile = os.path.join(root_dir, 'url.conf')
        # 配置是否断言失败后继续请求,默认为False,失败后停止执行
        self.is_continue = True

    @staticmethod
    def request_hook(r, *args, **kwargs):
        """
        钩子函数,可自定定义
        """
        print(f'request_hook: {r}')

    @staticmethod
    def response_hook(r, *args, **kwargs):
        """
        钩子函数,可自定定义
        """
        print(f'response_hook: {r}')

    @staticmethod
    def assertion_hook(r, *args, **kwargs):
        """
        钩子函数,可自定定义
        """
        print(f'assertion_hook: {r}')

    @staticmethod
    def associated_hook(r, *args, **kwargs):
        """
        钩子函数,可自定定义
        """
        print(f'associated_hook: {r}')

    @func_loop(2)
    def get_data(self):
        """
        必选步骤:1、4
        """
        # 1、需要请求哪些接口,可以使用列表标记出来,执行时会按列表顺序执行请求
        names = ['random', 'all']
        # 2、对配置文件中的请求头添加数据,根据配置文件中变量$${name}插入数据
        tripartite = {'random': {'timestamp': timestamp()},
                      'all': {'timestamp': timestamp()}}
        # 3、指定对应接口哪个位置执行钩子函数,可获得或修改钩子对象的值,共4种钩子
        hooks = {
            'register': {'request': self.request_hook, 'response': self.response_hook, 'assertion': self.assertion_hook,
                         'associated': self.associated_hook}}
        # 4、调用主方法发起请求
        self.main(names, tripartite=tripartite, hooks=hooks, proxies=self.proxies, timeout=5)


if __name__ == '__main__':
    api = Api()
    api.get_data()
