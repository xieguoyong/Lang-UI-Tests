import uiautomator2 as u2


# d = u2.connect("IP")   # 通过设备IP连接
d = u2.connect("W4D6LFTKDIHUUO4T")   # 通过设备号连接

"""***** get device info *****"""
print("设备信息： ", d.info)
print("设备屏幕分辨率： ", d.window_size())
print("设备序列号： ", d.serial)


"""***** get app info *****"""

print("获取当前运行app信息： ", d.app_current())

# # 获取app图标
# img = d.app_icon("com.lang.lang")
# img.save(r"C:\Users\Administrator\Desktop\icon.png")
