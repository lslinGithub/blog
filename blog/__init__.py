# 在这里引入app.py的Appconfig 来修改后端app的名称
from .apps import AppConfig
import os

default_app_config = 'blog.BlogConfig'  # 指定值来自apps.py中的类名BlogConfig


def get_current_app_name(_file):  # 获取当前应用名
    return os.path.split(os.path.dirname(_file))[-1]


class BlogConfig(AppConfig):  # 重写BlogConfig
    name = get_current_app_name(__file__)
    verbose_name = u'博客'
