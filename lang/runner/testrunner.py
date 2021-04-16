import unittest
import os
import sys
from lang.tools import HTMLTestRunner
from lang.tools import send_email
from lang.testcase.test_lang import MyTests

basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(basedir)


def add_suite(caselist):
    """指定执行某条case，用于单条case的调试，不用每次调试都执行所有case"""
    suite = unittest.TestSuite()
    suite.addTests(caselist)
    return suite


def add_case():
    """unittest.defaultTestLoader(): defaultTestLoader()类，
    通过该类下面的discover()方法可自动根据测试目录start_dir匹配查找测试用例文件（test*.py），
    并将查找到的测试用例组装到测试套件，因此可以直接通过run()方法执行discover"""

    case_dir = basedir + '/lang/testcase/'
    suite = unittest.defaultTestLoader.discover(case_dir, pattern='test_lang.py')
    return suite


def run_case(suite):
    """执行用例并生成报告"""
    report_path = basedir + "/lang/report/Report.html"
    fp = open(report_path, 'wb')

    """生成报告的Title,描述"""
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='【lang-QA环境】APP——UI自动化冒烟测试', description='测试用例执行结果如下所示：')
    runner.run(suite)
    fp.close()


if __name__ == '__main__':
    """这里执行所有case"""
    all_cases = add_case()
    run_case(all_cases)
    send_email.send_mail_report("【lang-QA环境】APP——UI自动化冒烟测试")

    # """这里执行指定的case"""
    # caselist = [MyTests("test_005_manage"), MyTests("test_006_mirror"), MyTests("test_007_exposure"), MyTests("test_008_cutaways")]
    # all_cases = add_suite(caselist)
    # run_case(all_cases)
    # # send_email.send_mail_report("【lang-QA环境】APP——UI自动化冒烟测试")
