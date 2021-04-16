import time


def change_env(d):
    """切换测试环境"""
    """长按切换环境按钮，打开选择环境面板"""
    d(resourceId="com.lang.lang:id/txt_env").long_click()
    time.sleep(3)
    d(resourceId="com.lang.lang:id/rb_env_qa").click()
    d(resourceId="com.lang.lang:id/btnSave").click()
    time.sleep(5)
