import os
import uiautomator2 as u2
import time
from lang.common.ini_read import *

# d = u2.connect("W4D6LFTKDIHUUO4T")   # 通过设备号连接
file_dir = r"E:\PycharmProject\Lang-UI-Test\apk"
app_package_name = ini_options('mobile', 'appPackage')


def get_apk_path():
    """提取apk名和路径"""
    file_name = os.listdir(file_dir)[0]
    file_path = os.path.join(file_dir, file_name)

    return file_path


def is_apk_installed():
    """检查apk是否已经安装过"""
    cmd_search_apk_package = "adb shell \"pm list package | grep " + app_package_name + "\""
    cmd_result = os.popen(cmd_search_apk_package).read()
    if app_package_name in cmd_result:
        print("原先安装过浪Live!!!")
        return True
    else:
        print("原先未安装过浪Live!!!")
        return False


def uninstall_app():
    """卸载app"""
    """如果安装过浪Live,则执行卸载，否则不执行"""
    if is_apk_installed() is True:
        cmd_uninstall = "adb uninstall " + app_package_name     # 拼装adb命令
        print("开始卸载浪Live!!!")
        os.system(cmd_uninstall)
    else:
        pass


def install_app(d):
    """安装app"""
    uninstall_app()     # 无论是否已安装，先执行卸载
    time.sleep(3)
    """os.system会阻塞进程，为避免不影响执行下一步，在命令前面一定要加start"""
    cmd_install = "start " + "adb install -r " + get_apk_path()        # 拼装adb命令
    print("开始安装浪Live!!!")
    os.system(cmd_install)
    time.sleep(3)
    try:
        """有时会弹出安装验证"""
        """弹出了验证的情况下，安装按钮会点不了，还不清楚什么情况！！"""
        verify_pwd = ini_options('mobile', 'verify_pwd')
        d(resourceId="com.coloros.safecenter:id/et_login_passwd_edit").send_keys(verify_pwd)
        d(text="安裝", resourceId="android:id/button1").click(timeout=5)
        time.sleep(7)
    except Exception as e:
        print(e)
        print("没有弹安装app验证!!!")

    d.click(0.445, 0.953)
    d.click(0.445, 0.953)       # 点击安装按钮（这里UI2定位不到，使用坐标定位）
    time.sleep(5)
    d(resourceId="com.android.packageinstaller:id/done_button").click()     # 点击完成
