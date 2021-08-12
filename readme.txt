框架说明：

apk：存放安装包  （暂时没用到）
config：存放配置信息
lang/common：存放公共方法 封装包等
lang/log：存放日志
lang/report：存放测试报告
lang/runner：存放运行脚本
lang/testcase：存放用例
lang/tools：存放公用包
lang/screenshot：存放截图


******************************************************************************************************
关于环境搭建：

# 如果本机未安装u2，需要先安装，命令行执行以下命令：
# pip install uiautomator2          # 安装u2
# python -m uiautomator2 init       # 在测试手机中自动安装atx, u2APK，需要先连接手机执行
# pip install --pre -U weditor      # 安装UI查看器
# python -m weditor                 # 启动UI查看器

需要用到的库：
pip install configparser            # 用于读取ini配置文件
pip sshtunnel                       # 用于ssh连接，通过ssh连接跳板机 然后再连接mysql
pip install pymysql                 # 用于连接mysql


*****************************************************************************************************
执行前须知：
1、需要提前将实际测试账号、手机IP等信息更新于配置文件UI2_config.ini
2、需要提前登录一个测试号（代码中是932900002）开播，这个测试号需要跟ui测试号（代码中是932900005）是好友关系，用于测试连麦PK、直播动态
3、在执行连麦PK用例的时候，需要在测试号中手动点击接受连麦邀请


*****************************************************************************************************
遇到的问题：
1、执行用例时报：RuntimeError: USB device 172.16.14.119 is offline
解决：重新初始化uiautomator2，然后重新执行用例
执行命令：python -m uiautomator2 init


获取toast信息的方法（参考test_027_follow_anchor用例）
self.d(text="追蹤成功").exists(timeout=10)