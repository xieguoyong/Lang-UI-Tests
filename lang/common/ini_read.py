from configparser import ConfigParser


class Myconf(ConfigParser):
    """默认的optionxform方法使得configParser读取配置文件时options会转化成小写
    这里重写optionxform方法，使得默认方法失效，即实现读取的options大小写不变"""

    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr):
        return optionstr


def ini_options(sections, option, ini_name='UI2_config'):
    """获取指定option的值"""
    """encoding="utf-8-sig"解决中文读取后乱码问题"""

    cfg = Myconf()
    if ini_name == 'UI2_config':
        cfg.read('E:\\PycharmProject\\Lang-UI-Test\\config\\UI2_config.ini', encoding="utf-8-sig")
        # cfg.sections()
        value = cfg.get(sections, option)
        return value
    elif ini_name == 'config':
        cfg.read('E:\\PycharmProject\\Lang-UI-Test\\config\\config.ini', encoding="utf-8-sig")
        # cfg.sections()
        value = cfg.get(sections, option)
        return value
    elif ini_name == 'element':
        cfg.read('E:\\PycharmProject\\Lang-UI-Test\\config\\element.ini', encoding="utf-8-sig")
        value = cfg.get(sections, option)
        return value
    elif ini_name == 'db':
        cfg.read('E:\\PycharmProject\\Lang-UI-Test\\config\\db.ini', encoding="utf-8-sig")
        value = cfg.get(sections, option)
        return value
    else:
        print("您ini_options方法没有传ini_name!!!!!!!!")


def ini_sections(sections):
    """获取section下所有信息，以dict返回"""

    cfg = Myconf()
    # cfg.read('E:\\PycharmProject\\Lang-UI-Test\\config\\config.ini')
    cfg.read('E:\\PycharmProject\\Lang-UI-Test\\config\\db.ini', encoding="utf-8-sig")
    value = cfg.items(sections)
    value = dict(value)
    return value
