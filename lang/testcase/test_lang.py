import time
import sys
import uiautomator2 as u2
import unittest
from lang.common.close_popup import *
from lang.common.ini_read import *
from lang.tools.log import logger as log
from lang.common.screenshot import screen_shot
from lang.common.app_manage import *
from lang.common.change_env import *


class MyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.uitestuser_phone = ini_options('users', 'uitestuser_phone')
        cls.verification_code = ini_options('users', 'verification_code')
        cls.testuser_name = ini_options('users', 'testuser_name')
        print("------------------开始执行UI自动化测试!!!------------------")
        """连接测试机"""
        # cls.d = u2.connect(ini_options('mobile', 'test_mobile_ip'))   # 通过IP连接.如果电脑和手机在同一wifi时可不连usb线直接wifi连
        cls.d = u2.connect(ini_options('mobile', 'device'))   # 通过设备号连接

        """app的安装、启动、切环境，需要时打开、不需要时可注释掉"""
        log.info("""开始安装浪Live!!!""")
        install_app(cls.d)

        log.info("开始启动app!!!")
        cls.d.app_start(ini_options('mobile', 'appPackage'))
        time.sleep(10)

        log.info("切换环境为-QA!!!")
        change_env(cls.d)

        log.info("启动监控弹窗提示的线程!!!")
        watch_popup(cls.d)

    # @unittest.skip("")
    @screen_shot
    def test_001_login(self):
        """手机验证登录"""
        log.info("开始手机验证登录!!!")
        self.d(resourceId="com.lang.lang:id/btnLoginPhoneRegister").click(timeout=5)
        self.d(resourceId="com.lang.lang:id/id_reg_phone").set_text(self.uitestuser_phone)
        self.d(resourceId="com.lang.lang:id/id_reg_code").set_text(self.verification_code)
        """关闭手机键盘"""
        close_panel(self.d)
        """点击登录"""
        self.d(resourceId="com.lang.lang:id/id_login_btn").click(timeout=5)
        time.sleep(10)
        # """关闭各种弹窗提示"""
        # close_popup(self.d)
        """根据直播标签名进行验证登录"""
        log.info("根据直播标签名进行验证登录")
        self.assertEqual('直播', self.d(resourceId="com.lang.lang:id/title", text="直播").get_text())

    # @unittest.skip("")
    @screen_shot
    def test_002_live(self):
        """秀场开播"""
        log.info("打开开播入口面板!!!")
        self.d(resourceId="com.lang.lang:id/img_bottom_bar_add").click(timeout=5)
        log.info("打开开播页面!!!")
        self.d(resourceId="com.lang.lang:id/to_live").click(timeout=5)
        # """关闭温馨提示弹窗"""
        # close_popup(self.d)
        time.sleep(5)
        log.info("选择分类!!!")
        self.d(text="音乐").click()
        log.info("关闭分享后开播!!!")
        self.d(resourceId="com.lang.lang:id/social_facebook").click(timeout=5)
        self.d(resourceId="com.lang.lang:id/torecord_start").click(timeout=5)
        time.sleep(10)
        """根据是否有更多操作按钮进行验证登录"""
        self.assertTrue(self.d(resourceId="com.lang.lang:id/rl_room_btn_more").exists())

    # @unittest.skip("")
    @screen_shot
    def test_003_noble(self):
        """贵宾席"""
        log.info("""打开贵宾席!!!""")
        self.d(resourceId="com.lang.lang:id/nobleSeatView").click(timeout=5)
        time.sleep(5)
        """根据贵宾席H5的title进行验证"""
        # self.assertEqual('貴賓席', self.d.xpath('//*[@resource-id="app"]/android.view.View[2]').get_text())
        self.assertTrue(self.d(text="貴賓席").exists(timeout=10))

    # @unittest.skip("")
    @screen_shot
    def test_004_luckdraw(self):
        """发起抽奖"""
        """关闭003打开的贵宾席"""
        close_panel(self.d)
        log.info("开始发起抽奖!!!")
        self.d(resourceId="com.lang.lang:id/rl_room_btn_more").click(timeout=5)
        self.d.xpath('//*[@resource-id="com.lang.lang:id/id_gridview"]/android.view.ViewGroup[4]').click(timeout=5)
        self.d(resourceId="com.lang.lang:id/et_gift_name").send_keys("UITest")
        self.d(resourceId="com.lang.lang:id/tv_gift_name").click(timeout=5)
        time.sleep(2)
        self.d.xpath('//*[@resource-id="com.lang.lang:id/id_gift_sublist"]/android.widget.RelativeLayout[7]/android.view.ViewGroup[1]/android.widget.ImageView[1]').click()
        self.d(resourceId="com.lang.lang:id/btn_lottery").click(timeout=5)
        """根据房间内抽奖挂件元素进行验证"""
        self.assertTrue(self.d(resourceId="com.lang.lang:id/id_room_lottery").exists(timeout=5))

    # @unittest.skip("")
    @screen_shot
    def test_005_manage(self):
        """管理"""
        self.d(resourceId="com.lang.lang:id/rl_room_btn_more").click(timeout=5)
        log.info("""打开管理面板!!!""")
        self.d.xpath('//*[@resource-id="com.lang.lang:id/id_gridview"]/android.view.ViewGroup[5]').click(timeout=5)
        time.sleep(2)
        log.info("""分别切换至’禁言列表’‘禁观看列表’‘管理员列表’!!!""")
        self.d(resourceId="com.lang.lang:id/psts_tab_title", text="禁言列表").click(timeout=5)
        self.d(resourceId="com.lang.lang:id/psts_tab_title", text="禁觀看列表").click(timeout=5)
        self.d(resourceId="com.lang.lang:id/psts_tab_title", text="管理員列表").click(timeout=5)
        """通过列表中用户昵称验证 （这里需要先将932900002设置成管理员）"""
        self.assertTrue(self.d(resourceId="com.lang.lang:id/id_name", text=self.testuser_name).exists(timeout=5))

    # @unittest.skip("")
    @screen_shot
    def test_006_mirror(self):
        """镜像"""
        """关闭005打开的管理面板,打开操作面板"""
        time.sleep(2)
        close_panel(self.d)
        self.d(resourceId="com.lang.lang:id/rl_room_btn_more").click(timeout=5)
        time.sleep(2)
        log.info("""关闭镜像!!!""")
        self.d.xpath('//*[@resource-id="com.lang.lang:id/id_gridview"]/android.view.ViewGroup[6]').click(timeout=5)
        """根据toast提示验证"""
        close_panel(self.d)
        # self.assertTrue(self.d(resourceId="com.lang.lang:id/id_topfloat_msg", text="已將觀眾鏡像模式關閉，觀眾與你看到的畫面是相反的").exists(timeout=5))
        self.assertTrue(self.d(resourceId="com.lang.lang:id/id_topfloat_msg").exists(timeout=5))
        time.sleep(3)
        self.d(resourceId="com.lang.lang:id/rl_room_btn_more").click(timeout=5)
        time.sleep(2)
        log.info("""打开镜像!!!""")
        self.d.xpath('//*[@resource-id="com.lang.lang:id/id_gridview"]/android.view.ViewGroup[6]').click(timeout=5)
        """根据toast提示验证"""
        close_panel(self.d)
        # self.assertTrue(self.d(resourceId="com.lang.lang:id/id_topfloat_msg", text="已將觀眾切換到鏡像模式，觀眾與你看到的畫面是一樣的了").exists(timeout=5))
        self.assertTrue(self.d(resourceId="com.lang.lang:id/id_topfloat_msg").exists(timeout=5))

    # @unittest.skip("")
    @screen_shot
    def test_007_exposure(self):
        """曝光"""
        time.sleep(3)
        self.d(resourceId="com.lang.lang:id/rl_room_btn_more").click(timeout=5)
        log.info("""切至手动曝光!!!""")
        self.d.xpath('//*[@resource-id="com.lang.lang:id/id_gridview"]/android.view.ViewGroup[7]').click(timeout=5)
        """根据toast提示验证"""
        close_panel(self.d)
        # self.assertTrue(self.d(resourceId="com.lang.lang:id/id_topfloat_msg", text="已開啟手動對焦曝光設定").exists(timeout=5))
        self.assertTrue(self.d(resourceId="com.lang.lang:id/id_topfloat_msg").exists(timeout=5))
        time.sleep(3)
        self.d(resourceId="com.lang.lang:id/rl_room_btn_more").click(timeout=5)
        log.info("""切至自动曝光!!!""")
        self.d.xpath('//*[@resource-id="com.lang.lang:id/id_gridview"]/android.view.ViewGroup[7]').click(timeout=5)
        """根据toast提示验证"""
        close_panel(self.d)
        # self.assertTrue(self.d(resourceId="com.lang.lang:id/id_topfloat_msg", text="已開啟自動對焦曝光設定").exists(timeout=5))
        self.assertTrue(self.d(resourceId="com.lang.lang:id/id_topfloat_msg").exists(timeout=5))

    # @unittest.skip("")
    @screen_shot
    def test_008_cutaways(self):
        """切换镜头"""
        self.d(resourceId="com.lang.lang:id/rl_room_btn_more").click(timeout=5)
        log.info("""切换后置摄像头!!!""")
        self.d.xpath('//*[@resource-id="com.lang.lang:id/id_gridview"]/android.view.ViewGroup[8]').click(timeout=5)
        time.sleep(3)
        log.info("""切回前置摄像头!!!""")
        self.d.xpath('//*[@resource-id="com.lang.lang:id/id_gridview"]/android.view.ViewGroup[8]').click(timeout=5)
        close_panel(self.d)

    # @unittest.skip("")
    @screen_shot
    def test_009_sendmessage(self):
        """发言"""
        log.info("发聊天消息!!!")
        self.d(resourceId="com.lang.lang:id/rl_room_btn_more").click(timeout=5)
        self.d.xpath('//*[@resource-id="com.lang.lang:id/id_gridview"]/android.view.ViewGroup[9]').click(timeout=5)
        """这里输入框应该是edittext_chat元素，而不是layout_chat"""
        # self.d(resourceId="com.lang.lang:id/layout_chat").send_keys("UITest")
        self.d(resourceId="com.lang.lang:id/edittext_chat").send_keys("UITest")
        self.d(resourceId="com.lang.lang:id/btn_send").click(timeout=5)
        time.sleep(3)
        """根据聊天区是否显示UITest来验证"""
        self.assertTrue(self.d(textContains='UITest', resourceId='com.lang.lang:id/room_chatitem_msg'))

    # @unittest.skip("")
    @screen_shot
    def test_010_livePK(self):
        """连播PK"""
        """发起连播PK，这里需要先在另一台手机用账号932900002开播 并在被邀请PK时接受，后面看是否可优化为自动"""
        self.d(resourceId="com.lang.lang:id/rl_room_btn_more").click(timeout=5)
        self.d.xpath('//*[@resource-id="com.lang.lang:id/id_gridview"]/android.view.ViewGroup[10]').click(timeout=5)
        log.info("发起好友PK!!!")
        self.d(resourceId="com.lang.lang:id/id_friend_pk_container").click(timeout=5)
        time.sleep(3)
        self.d(resourceId="com.lang.lang:id/invite").click(timeout=5)
        # log.info("""关闭PK提示!!!""")
        # close_popup_livePK(self.d)
        self.d(resourceId="com.lang.lang:id/invite").click(timeout=5)
        time.sleep(30)
        """根据用户席位元素进行验证"""
        self.assertTrue(self.d(resourceId="com.lang.lang:id/pk_contribution_view").exists())
        # time.sleep(120)
        # log.info("""结束连麦!!!""")
        # """这里因为巅峰段位按钮和连麦关闭按钮重叠了，使用点击按钮无法生效，先用点击按钮坐标的方式解决"""
        # # self.d(resourceId="com.lang.lang:id/link_mic_status").click()
        # close_panel(self.d)
        # self.d(resourceId="com.lang.lang:id/positiveButton").click(timeout=5)

    # @unittest.skip("")
    @screen_shot
    def test_011_knapsack(self):
        """背包"""
        log.info("""打开背包!!!""")
        self.d(resourceId="com.lang.lang:id/rl_room_btn_more").click(timeout=5)
        self.d.xpath('//*[@resource-id="com.lang.lang:id/id_gridview"]/android.view.ViewGroup[12]').click(timeout=5)
        time.sleep(1)
        """根据背包里的小血包进行验证（如果账号没有小血包道具，可根据实际情况修改验证方式）"""
        self.assertEqual('小血包', self.d(resourceId="com.lang.lang:id/id_bag_title", text="小血包").get_text())

    # @unittest.skip("")
    @screen_shot
    def test_012_Stickers(self):
        """装饰贴纸"""
        """先关闭011打开的背包面板"""
        close_panel(self.d)
        log.info("""打开装饰贴纸面板!!!""")
        self.d(resourceId="com.lang.lang:id/rl_room_btn_more").click(timeout=5)
        self.d.xpath('//*[@resource-id="com.lang.lang:id/id_gridview"]/android.view.ViewGroup[15]').click(timeout=5)
        self.d(resourceId="com.lang.lang:id/txt_name", text="守護金牛").click(timeout=5)
        """根据房间内贴纸元素验证"""
        self.assertTrue(self.d(resourceId="com.lang.lang:id/id_room_decorate_stamp_view").exists(timeout=5))
        # """关闭贴纸"""
        # self.d(resourceId="com.lang.lang:id/iv_decorate_stamp_close").click()

    # @unittest.skip("")
    @screen_shot
    def test_013_redpacket(self):
        """发红包"""
        log.info("""开始发红包!!!""")
        self.d(resourceId="com.lang.lang:id/rl_room_btn_more").click(timeout=5)
        self.d.xpath('//*[@resource-id="com.lang.lang:id/id_gridview"]/android.view.ViewGroup[17]').click(timeout=5)
        time.sleep(3)
        self.d.xpath('//*[@resource-id="com.lang.lang:id/redpacket_list"]/android.widget.RelativeLayout[3]').click(timeout=5)
        time.sleep(3)
        # 这个确认提示会被弹框监控执行，这里不需要再操作
        # self.d(resourceId="com.lang.lang:id/positiveButton").click(timeout=5)
        """根据弹出红包的抢红包按钮进行验证"""
        self.assertTrue(self.d(resourceId="com.lang.lang:id/id_redpacket_mid_open").exists(timeout=5))

    # @unittest.skip("")
    @screen_shot
    def test_014_privateletter(self):
        """私信"""
        """**********************如果测试账号有改，这里的验证信息要修改*******************"""
        """这里缺少发私信消息的case，后续添加"""
        """先关闭013发的红包"""
        if self.d(resourceId="com.lang.lang:id/id_redpacket_top_bar_close").exists(timeout=5):
            self.d(resourceId="com.lang.lang:id/id_redpacket_top_bar_close").click(timeout=5)

        log.info("""打开私信面板!!!""")
        self.d.xpath(
            '//*[@resource-id="com.lang.lang:id/id_room_bottom_container"]/android.widget.RelativeLayout[1]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]').click(timeout=5)
        """根据是否显示小秘书验证"""
        self.assertEqual('浪Live小秘書', self.d(resourceId="com.lang.lang:id/id_msg_title", text="浪Live小秘書").get_text())
        log.info("""切至群组tab!!!""")
        self.d.xpath(
            '//*[@resource-id="com.lang.lang:id/id_sliding_tab_container"]/android.widget.RelativeLayout[2]/android.widget.RelativeLayout[1]/android.view.View[1]').click(timeout=5)
        """根据群组名称验证"""
        self.assertEqual('浪客_1049691测试 的粉絲群組', self.d(resourceId="com.lang.lang:id/id_msg_title", text="浪客_1049691测试 的粉絲群組").get_text())

    # @unittest.skip("")
    @screen_shot
    def test_015_luckywheel(self):
        """转盘"""
        """先关闭014打开的私信面板"""
        close_panel(self.d)
        log.info("""打开转盘面板!!!""")
        self.d(resourceId="com.lang.lang:id/id_lucky_wheel_icon").click(timeout=5)
        time.sleep(5)
        log.info("""开始幸运转盘抽奖!!!""")
        self.d(text="lucky-wheel-start-btn.4ee1a07").click(timeout=5)
        time.sleep(20)
        """根据抽奖结果的'再抽1次'按钮验证"""
        self.assertEqual('再抽1次', self.d(text="再抽1次").get_text())
        """关闭抽奖结果面板"""
        close_panel(self.d)
        log.info("""切至黄金转盘面板!!!""")
        self.d.xpath(
            '//*[@resource-id="app"]/android.view.View[1]/android.view.View[3]/android.view.View[1]/android.view.View[2]').click(timeout=5)
        time.sleep(5)
        log.info("""开始黄金转盘抽奖!!!""")
        self.d(text="gold-wheel-start-btn.7b52608").click(timeout=5)
        time.sleep(20)
        """根据抽奖结果的'再抽1次'按钮验证"""
        self.assertEqual('再抽1次', self.d(text="再抽1次").get_text())

    # @unittest.skip("")
    @screen_shot
    def test_016_faceu(self):
        """脸部 手势特效"""
        """先关闭015打开的抽奖结果面板、转盘面板"""
        close_panel(self.d, 2)
        log.info("""打开faceu面板!!!""")
        self.d(resourceId="com.lang.lang:id/id_faceu").click(timeout=5)
        time.sleep(2)
        """因为tab会保存在上次切换的tab，这里先将tab定位至faceu"""
        self.d(description="臉部特效").click(timeout=5)
        log.info("""选中第一个faceu!!!""")
        """这里点击两次，模拟第一次下载、第二次使用"""
        self.d.xpath('//*[@resource-id="com.lang.lang:id/face_list"]/android.widget.RelativeLayout[2]').click(timeout=5)
        log.info("""选中第二个faceu!!!""")
        self.d.xpath('//*[@resource-id="com.lang.lang:id/face_list"]/android.widget.RelativeLayout[2]').click(timeout=5)
        """这里模拟切换faceu"""
        self.d.xpath('//*[@resource-id="com.lang.lang:id/face_list"]/android.widget.RelativeLayout[3]').click(timeout=5)
        self.d.xpath('//*[@resource-id="com.lang.lang:id/face_list"]/android.widget.RelativeLayout[3]').click(timeout=5)
        """关闭faceu面板，看效果"""
        close_panel(self.d)
        log.info("""再次打开faceu面板，切至手势tab!!!""")
        self.d(resourceId="com.lang.lang:id/id_faceu").click(timeout=5)
        time.sleep(2)
        self.d(description="手勢特效").click(timeout=5)
        log.info("""选中第一个手势!!!""")
        """这里点击两次，模拟第一次下载、第二次使用"""
        self.d.xpath('//*[@resource-id="com.lang.lang:id/face_list"]/android.widget.RelativeLayout[2]').click(timeout=5)
        self.d.xpath('//*[@resource-id="com.lang.lang:id/face_list"]/android.widget.RelativeLayout[2]').click(timeout=5)
        log.info("""切至'托手'tab！！！""")
        self.d.xpath('//*[@resource-id="com.lang.lang:id/faceu_sub_tab"]/android.widget.RelativeLayout[2]').click(timeout=5)
        time.sleep(2)
        """根据'天秤寶寶'的手势名称验证"""
        self.assertEqual('天秤寶寶', self.d(resourceId="com.lang.lang:id/faceu_name", text="天秤寶寶").get_text())
        """关闭faceu面板"""
        close_panel(self.d)

    # @unittest.skip("")
    @screen_shot
    def test_017_closeroom(self):
        """秀场关播"""
        log.info("准备关播!!!")
        self.d(resourceId="com.lang.lang:id/id_room_close").click(timeout=5)
        time.sleep(1)
        self.d(resourceId="com.lang.lang:id/positiveButton").click(timeout=5)
        """根据结束页面的关闭按钮进行验证登录"""
        self.assertIsNotNone(self.d(resourceId="com.lang.lang:id/torecord_close_btn"))
        log.info("关闭结束页面返回秀场首页!!!")
        self.d(resourceId="com.lang.lang:id/torecord_close_btn").click(timeout=5)
        self.d(resourceId="com.lang.lang:id/id_room_lottery").exists(timeout=5)

    # @unittest.skip("")
    @screen_shot
    def test_020_snslive(self):
        """直播动态"""
        log.info("""打开直播动态页面!!!""")
        self.d(resourceId="com.lang.lang:id/home_sns_live").click()
        """根据主播932900002的昵称来验证"""
        self.assertEqual(self.testuser_name, self.d(resourceId="com.lang.lang:id/id_name", text=self.testuser_name).get_text())

    # @unittest.skip("")
    @screen_shot
    def test_021_enterroom(self):
        """从直播动态进入直播间"""
        log.info("""进入直播间""")
        self.d(resourceId="com.lang.lang:id/id_name", text=self.testuser_name).click()
        time.sleep(5)
        """通过直播间左上角主播昵称来验证"""
        self.assertEqual(self.testuser_name, self.d(resourceId="com.lang.lang:id/tv_user_name", text=self.testuser_name).get_text())

    # @unittest.skip("")
    @screen_shot
    def test_022_sendmsg(self):
        """用户发消息"""
        log.info("""发消息'UITest2'!!!""")
        self.d(resourceId="com.lang.lang:id/id_room_btn_send").click()
        self.d(resourceId="com.lang.lang:id/edittext_chat").send_keys("UITest2")
        self.d(resourceId="com.lang.lang:id/btn_send").click()
        time.sleep(2)
        """根据聊天区是否显示UITest2来验证"""
        self.assertTrue(self.d(textContains='UITest2', resourceId='com.lang.lang:id/room_chatitem_msg').exists())

    # @unittest.skip("")
    @screen_shot
    def test_023_open_giftpanel(self):
        """打开礼物面板"""
        log.info("""打开礼物面板""")
        self.d(resourceId="com.lang.lang:id/id_room_bottom_gift_container").click()
        time.sleep(2)
        """先定位到推荐栏"""
        self.d(text='推薦', resourceId="com.lang.lang:id/tv_tab_name").click()
        """根据推荐栏title验证"""
        self.assertTrue(self.d(text='推薦', resourceId='com.lang.lang:id/tv_tab_name').exists())
        """根据礼物栏礼物数量不为0验证礼物加载"""
        self.assertNotEqual('0', self.d(resourceId='com.lang.lang:id/id_gift_cover').count)

    # @unittest.skip("")
    @screen_shot
    def test_024_change_giftpanel(self):
        """切换礼物栏&背包"""
        log.info("""切换礼物栏""")
        self.d(text='经典', resourceId="com.lang.lang:id/tv_tab_name").click()
        time.sleep(1)
        self.assertNotEqual('0', self.d(resourceId='com.lang.lang:id/id_gift_cover').count)
        self.d(text='貴族', resourceId="com.lang.lang:id/tv_tab_name").click()
        time.sleep(1)
        self.assertNotEqual('0', self.d(resourceId='com.lang.lang:id/id_gift_cover').count)
        self.d(text='週星', resourceId="com.lang.lang:id/tv_tab_name").click()
        time.sleep(1)
        self.assertNotEqual('0', self.d(resourceId='com.lang.lang:id/id_gift_cover').count)

        """切换背包"""
        log.info("""切换背包""")
        self.d(resourceId="com.lang.lang:id/bagButton").click()
        """根据背包礼物栏title验证"""
        self.assertTrue(self.d(text='背包禮物', resourceId='com.lang.lang:id/tv_tab_name').exists())
        """根据礼物栏礼物数量不为0验证礼物加载"""
        self.assertNotEqual('0', self.d(resourceId='com.lang.lang:id/id_gift_cover').count)

        """切回礼物栏"""
        self.d(resourceId="com.lang.lang:id/giftButton").click()

    # @unittest.skip("")
    @screen_shot
    def test_025_sendgift(self):
        """用户送礼"""
        time.sleep(2)
        log.info("""选中推荐栏第1个礼物""")
        self.d.xpath('//*[@resource-id="com.lang.lang:id/id_gift_sublist"]/android.widget.RelativeLayout[1]').click()
        log.info("""获取礼物价格、名字、浪花数，用于后面验证""")
        gift_price = self.d(resourceId="com.lang.lang:id/id_gift_price").get_text()
        gift_name = self.d(resourceId="com.lang.lang:id/giftDescriptionName").get_text()
        spray_value = self.d(resourceId="com.lang.lang:id/id_moneyinfo_value").get_text()
        surplus_spray_value = int(spray_value) - int(gift_price)
        log.info("礼物价格-> {}，礼物名称-> {}，送礼前浪花数-> {}".format(gift_price, gift_name, spray_value))
        log.info("""点击送礼""")
        self.d(resourceId="com.lang.lang:id/id_room_gift_send").click()
        time.sleep(3)
        """根据聊天区是否显示礼物名称验证"""
        self.assertTrue(self.d(textContains=gift_name, resourceId='com.lang.lang:id/room_chatitem_msg').exists(timeout=5))
        """再次打开礼物面板，以验证扣除浪花数是否正确"""
        self.d(resourceId="com.lang.lang:id/id_room_bottom_gift_container").click()
        time.sleep(2)
        """由于浪花数不会实时更新，这里先进入浪花储值页面再返回，更新浪花后再获取"""
        self.d(resourceId="com.lang.lang:id/id_gift_langhua").click()
        time.sleep(5)
        self.d(resourceId="com.lang.lang:id/id_top_bar_left_img").click()
        time.sleep(2)
        after_spray_value = self.d(resourceId="com.lang.lang:id/id_moneyinfo_value").get_text()
        log.info("""送礼后浪花数-> {}""".format(after_spray_value))
        self.assertEqual(str(surplus_spray_value), after_spray_value)

    # @unittest.skip("")
    @screen_shot
    def test_026_anchor_card(self):
        """查看主播名片"""
        """先关闭之前打开的礼物面板"""
        close_panel(self.d)
        log.info("""打开主播名片""")
        self.d(resourceId="com.lang.lang:id/iv_anchor_head").click(timeout=5)
        time.sleep(2)
        """根据主播名片的主播昵称验证"""
        self.assertTrue(self.d(text=self.testuser_name, resourceId="com.lang.lang:id/name").exists(timeout=5))

    # @ unittest.skip("")
    @screen_shot
    def test_027_anchor_homepage(self):
        """查看主播个人主页"""
        log.info("""打开主播个人主页""")
        self.d(resourceId="com.lang.lang:id/userPhoto").click(timeout=5)
        time.sleep(2)
        """根据主播名片的主播昵称验证"""
        self.assertTrue(
            self.d(text=self.testuser_name, resourceId="com.lang.lang:id/id_user_center_user_name").exists(
                timeout=5))
        """返回直播间"""
        self.d(resourceId="com.lang.lang:id/id_user_center_left").click(timeout=5)

    # @unittest.skip("")
    @screen_shot
    def test_028_unfollow_anchor(self):
        """取消关注主播"""
        time.sleep(2)
        # """上面返回后会有一个蒙层，导致不能定位到名片，这里先关闭主播名片再重新打开"""
        # close_panel(self.d)
        self.d(resourceId="com.lang.lang:id/iv_anchor_head").click(timeout=5)
        """如果原来未关注过，先关注之后再取消"""
        if self.d(resourceId="com.lang.lang:id/follow").get_text() == '追蹤':
            self.d(resourceId="com.lang.lang:id/follow").click(timeout=5)
            time.sleep(3)

        log.info("""取消关注主播!!!""")
        self.d(resourceId="com.lang.lang:id/follow").click(timeout=5)
        """需要先关闭名片，否则获取不到toast信息"""
        close_panel(self.d)
        """通过弹出toast提示验证"""
        self.assertTrue(self.d(text="取消追蹤成功").exists(timeout=5))

    # @unittest.skip("")
    @screen_shot
    def test_029_follow_anchor(self):
        """关注主播"""
        """上面关闭了名片，这里需要再次打开"""
        time.sleep(2)
        self.d(resourceId="com.lang.lang:id/iv_anchor_head").click(timeout=5)
        """如果原来已经关注过了，先取消之后再进行关注"""
        if self.d(resourceId="com.lang.lang:id/follow").get_text() == '取消追蹤':
            self.d(resourceId="com.lang.lang:id/follow").click(timeout=5)
            time.sleep(3)

        log.info("""关注主播!!!""")
        self.d(resourceId="com.lang.lang:id/follow").click(timeout=5)
        """需要先关闭名片，否则获取不到toast信息"""
        close_panel(self.d)
        """通过弹出toast提示验证"""
        self.assertTrue(self.d(text="追蹤成功").exists(timeout=5))

    # @ unittest.skip("")
    @screen_shot
    def test_030_top_rank(self):
        """巅峰段位"""
        time.sleep(2)
        """获取主播段位"""
        top_rank = self.d(resourceId="com.lang.lang:id/tv_top_rank").get_text()
        log.info("""打开巅峰段位面板""")
        self.d(resourceId="com.lang.lang:id/tv_top_rank").click()
        """根据面板中段位等级验证"""
        self.assertEqual(top_rank, self.d(resourceId="com.lang.lang:id/currentStageText").get_text())

    # @ unittest.skip("")
    @screen_shot
    def test_031_top_value(self):
        """送礼增加巅峰值"""
        current_top_value = self.d(resourceId="com.lang.lang:id/currentRankValue").get_text()
        current_top_value = current_top_value.replace(',', '')
        log.info("获取主播当前巅峰值--> {}".format(current_top_value))
        log.info("""用户开始送礼!!!""")
        """关闭巅峰段位面板，打开礼物面板"""
        close_panel(self.d)
        self.d(resourceId="com.lang.lang:id/id_room_bottom_gift_container").click(timeout=5)
        time.sleep(2)
        gift_price = self.d(resourceId="com.lang.lang:id/id_gift_price").get_text()
        log.info("获取礼物价格--> {}".format(gift_price))
        """赠送礼物"""
        self.d(resourceId="com.lang.lang:id/id_room_gift_send").click(timeout=5)
        expect_top_value = int(current_top_value) + int(gift_price) * float(ini_options('top_value', 'addition'))
        log.info("预期送礼后主播巅峰值--> {}".format(expect_top_value))
        log.info("""再次打开巅峰段位面板!!!""")
        self.d(resourceId="com.lang.lang:id/tv_top_rank").click()
        time.sleep(2)
        after_top_value = self.d(resourceId="com.lang.lang:id/currentRankValue").get_text()
        after_top_value = after_top_value.replace(',', '')
        log.info("实际送礼后主播巅峰值--> {}".format(after_top_value))
        self.assertEqual(int(expect_top_value), int(after_top_value))
        """关闭主播巅峰段位面板"""
        close_panel(self.d)

    # @ unittest.skip("")
    @screen_shot
    def test_032_exit_room(self):
        """退出房间"""
        log.info("""点击右上角退出房间按钮!!!""")
        self.d(resourceId="com.lang.lang:id/id_room_close").click()
        time.sleep(2)
        """因返回的是直播动态页面，这里根据页面title验证"""
        self.assertTrue(self.d(text="追蹤").exists(timeout=5))

    @classmethod
    def tearDownClass(cls):
        time.sleep(5)
        print("------------------UI自动化测试结束!!!----------------------")
        # cls.d.app_stop("com.lang.lang")


if __name__ == '__main__':
    unittest.main()
