"""
@Time    : 2024/8/10 17:53
@Author  : YueJiang
@File    : handle_live_mean_nc.py
@Software: PyCharm
"""


def check_none(*args):
    """
    有一个参数为None就返回true
    :param args: 可变参数
    :return: bool
    """
    return any(arg is None for arg in args)
