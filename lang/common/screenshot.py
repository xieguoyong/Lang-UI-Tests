from functools import wraps
import os
import time
from lang.tools.log import logger as log


def screen_shot(function):
    @wraps(function)
    def get_error_img(self, *args, **kwargs):
        try:
            result = function(self, *args, **kwargs)
        except AssertionError as e:
            log.info(e)
            case_name = function.__name__
            proj_path = os.path.dirname(os.path.dirname(__file__))
            image_path = os.path.join(proj_path, 'screenshot')
            image_name = os.path.join(image_path, case_name + '--{}.jpg'.format(time.strftime('%Y-%m-%d--%H_%M_%S')))
            img = self.d.screenshot()
            img.save(image_name)
            """这里不加的话fail也会返回pass，还没整明白原因，先强行判定为False处理"""
            assert False
        else:
            return result
    return get_error_img
