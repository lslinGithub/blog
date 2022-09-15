from .apps import AppConfig
import os

default_app_config = 'comments.CommentsConfig'


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class CommentsConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = u'评论'
