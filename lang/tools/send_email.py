import smtplib
import os, zipfile, time
import sys
"""发送纯文本信息"""
from email.mime.text import MIMEText
"""混合信息"""
from email.mime.multipart import MIMEMultipart
"""导入配置库"""
from lang.common.ini_read import *

basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(basedir)


# def zip_report(input_path, output_path, output_name):
#     """将测试报告生成压缩文件"""
#     f = zipfile.ZipFile(output_path+'/' + output_name, 'w', zipfile.ZIP_DEFLATED)
#     files = os.listdir(input_path)
#     for file in files:
#         if os.path.splitext(file)[1] == ".html":
#             f.write(input_path + '/' + file)
#             f.close()
#     return output_path+r"/"+output_name


def send_mail_report(title):
    """将测试报告发送到邮件"""

    """获取测试报告邮件服务器、发件人、收件人等信息"""
    """发件人"""
    sender = ini_options('mail', 'sender', 'config')
    """收件人"""
    receiver = ini_options('mail', 'receiver', 'config')
    """smtp服务器"""
    smtp_server = ini_options('mail', 'smtp_server', 'config')
    """smtp服务端口"""
    mail_port = ini_options('mail', 'mail_port', 'config')
    """账户"""
    username = ini_options('mail', 'username', 'config')
    """密码"""
    password = ini_options('mail', 'password', 'config')

    msg_root = MIMEMultipart("related")
    msg_root["subject"] = title
    msg_root["from"] = sender
    msg_root["to"] = receiver
    body = "hi, All! 附件为交易网关业务功能【QA环境】版本接口测试报告，请注意查看！"
    msg_html = MIMEText(body, 'html', 'utf-8')
    msg_root.attach(msg_html)

    """获取最新测试报告"""
    report_path = basedir+"/lang/report/"
    new_report = ""
    for root, subdirs, files in os.walk(report_path):
        for file in files:
            """判断该目录下的文件扩展名是否为html"""
            if os.path.splitext(file)[1] == ".html":
                new_report = file

    # """改变当前的相对路径由 testSuite变更为report,然后压缩report下面的测试报告Report.html文件"""
    # os.chdir(report_path)
    # cwd = os.getcwd()
    # print("cwd is:"+cwd)
    # """将Report.html文件压缩成.zip文件，存放路径为./report"""
    # zip_report(r"./", './', 'payCenter_API_Test_Report.zip')

    """生成邮件的内容"""
    msg = MIMEMultipart()
    msg["subject"] = title
    msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')
    with open(os.path.join(report_path, new_report), 'rb') as f:
        mailbody = f.read()
    html = MIMEText(mailbody, _subtype='html', _charset='utf-8')
    msg.attach(html)

    """将测试报告压缩文件添加到邮件附件"""
    # att = MIMEText(open('./payCenter_API_Test_Report.zip', 'rb').read(), 'base64', 'utf-8')
    att = MIMEText(open(os.path.join(report_path, new_report), 'rb').read(), 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att.add_header("Content-Disposition", "attachment", filename="Report.html")
    msg.attach(att)

    """发送邮件"""
    msg['from'] = sender
    try:
        smtp = smtplib.SMTP_SSL(smtp_server, 465)
        # smtp = smtplib.SMTP()
        # smtp.connect(smtp_server, mail_port)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver.split(','), msg.as_string())
        smtp.close()
        print("邮件发送成功")
    except Exception:
        print("Error :无法发送邮件")
        raise


if __name__ == '__main__':
    send_mail_report("【lang-QA环境】APP——UI自动化冒烟测试")
