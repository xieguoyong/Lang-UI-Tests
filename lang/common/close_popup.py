
def close_popup(d):
    """关闭登录后各种弹窗提示"""
    while True:
        if d(resourceId="com.lang.lang:id/id_close").exists(timeout=1):
            """登录后的2019弹窗"""
            d(resourceId="com.lang.lang:id/id_close").click()
            continue
        elif d(resourceId="com.lang.lang:id/daily_sign_close").exists(timeout=1):
            """登录后的签到提示"""
            d(resourceId="com.lang.lang:id/daily_sign_close").click()
            continue
        elif d(resourceId="com.lang.lang:id/negativeButton").exists(timeout=1):
            """登录后的本日推荐提示"""
            d(resourceId="com.lang.lang:id/negativeButton").click()
            continue
        elif d(resourceId="com.lang.lang:id/positiveButton").exists(timeout=1):
            """开播前温馨提示，开启系统权限"""
            d(resourceId="com.lang.lang:id/positiveButton").click()
            d(resourceId="com.android.permissioncontroller:id/permission_allow_button").click(timeout=2)
            continue
        else:
            break


def close_popup_livePK(d):
    """关闭连麦PK的提示"""
    if d(resourceId="com.lang.lang:id/positiveButton").exists(timeout=1):
        d(resourceId="com.lang.lang:id/positiveButton").click()
    else:
        pass


def close_panel(d, num=1):
    """
    实现点击空白处关闭弹出的面板，有的功能会弹出多层面板，因此这里根据num执行点击次数
    :param num: 要关闭面板的数量
    :param d: 连接对象
    """
    for i in range(num):
        d.click(0.713, 0.178)


def swipe_screen(d, direction="right"):
    """
    实现整个屏幕左右划动(默认为向右划)，可用于关闭各种弹出面板等场景
    :param direction: 划动方向
    :param d: 连接对象
    """
    """测试发现该方法有风险，如果前一操作因异常没有弹出面板，此时执行划屏操作可能导致退出app"""
    """需要优化一下，先检测如果有弹出面板才去执行此方法"""
    if direction == "right":
        d.swipe_ext("right", scale=0.9)
    elif direction == "left":
        d.swipe_ext("left", scale=0.9)
    else:
        print("您没有选择划屏方向！！")


def swipe_until(d):
    """实现一直划屏，直到可以定位到某个元素"""
    while True:
        swipe_screen(d)
        if d(textContains="八八六十", resourceId="com.lang.lang:id/tv_user_name").wait(timeout=3):
            break


# 监听弹窗
def watch_popup(d):
    """实现关闭各种弹窗提示"""
    try:
        ctx = d.watch_context()
        # 登录后弹出的2019专属回忆提示
        # 通过底部关闭按钮x关闭
        ctx.when("com.lang.lang:id/id_close").click()

        # 登录后弹出的日间签到提示
        # 通过右上角关闭按钮x关闭
        ctx.when("com.lang.lang:id/daily_sign_close").click()

        # 登录后弹出的本日推荐提示
        # 新功能[本日推薦]上線囉，想要看到更多的推薦主播，需要您的協助給予權限
        ctx.when("前往").when("我知道了").click()

        ctx.wait_stable()  # 等待界面不在有弹窗了

        # 开播前弹出的温馨提示，开启相关权限（安装app后第一次登录前也会弹；第一次登录后也会弹）
        # 由於您即將要開播，需要您允許以下的權限喔 -拍攝及錄影 -存取裝置中的檔案 -允許定位服務
        ctx.when("繼續").click()
        ctx.when("取消").when("確定").click()  # 开播前提示，点继续后会弹 取消/确定 # 连播PK的弹出提示也是用的这个
        ctx.when("允許").click()  # 登录前提示，点继续后会弹 拒绝/允许

        ctx.wait_stable()  # 等待界面不在有弹窗了

        # 直播间弹出碎片合成弹窗提示
        ctx.when("去合成").when("取消").click()
        # 直播间弹出网络异常弹窗提示
        ctx.when("取消").when("重新載入").click()

        # 导航栏点击私信 弹出的提示
        # “建議開啟應用程式通知功能 好友發出的訊息會通知您哦！”
        ctx.when("去開啟").when("取消").click()

        # 导航栏点击个人中心弹出的领取现金提示
        # 無限量賺現金模式已開啟
        # 通过右上角关闭按钮x关闭
        ctx.when("恭喜你").when("com.lang.lang:id/dialog_close").click()

        ctx.wait_stable()  # 等待界面不在有弹窗了

    except Exception as e:
        print(e)

    # d.ctx.close()
