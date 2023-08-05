from functools import wraps
import logging

logger = logging.getLogger("tasks")


def edit_base(fun):
    """用于统一返回值，如果失败返回500状态码"""

    @wraps(fun)
    def wrapper(*args, **kwargs):
        try:
            msg = fun(*args, **kwargs)
            response = {'code': 200, 'message': msg, 'data': str(msg)}
        except Exception as e:
            logger.error('连接云sdk失败，错误代码为{}'.format(e))
            response = {'code': 500, 'message': str(e)}  # e转成字符串，便于返回报错信息
        print(response)
        return response

    return wrapper
