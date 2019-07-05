import sys
sys.path.append(r'E:\Auto_frame')
import unittest
from utils.config import REPORT_PATH,Config,DATA_PATH
from utils.client import HTTPClient
from utils.log import logger
from utils.HTMLTestRunner import HTMLTestRunner
from utils.assertion import assertHTTPCode
from utils.file_reader import ExcelReader
import json
from utils.get_excel_data import Excel_Data
from utils.mail import Email


class TestUserAPI(unittest.TestCase):
    excel_path = DATA_PATH + '\\api.xls'
    API_UTL = Config().get('API_URL')
    excel_data = Excel_Data().excel_data()


    def test_login_01(self):
        '''测试接口'''
        datas = ExcelReader(self.excel_path).data
        for d in datas:
            if d['run'].lower() == 'yes':
                with self.subTest(data=d['describe']):
                    url = self.API_UTL + d['api']
                    method = d['method']
                    data = d['data']
                    #判断excel上面的data不为空时执行获取datas,否则执行不传data的get方法
                    if data != '':
                        datas = self.excel_data[data]
                        if method == 'post':
                            res = HTTPClient(url=url, method=method).send(data=datas).json()
                        else:
                            res = HTTPClient(url=url, method=method).send(params=datas).json()
                    else:
                        res = HTTPClient(url=url, method=method).send().json()

                    logger.debug('响应code字段:%s'% res['code'])
                    assertHTTPCode(res)   #判断响应json数据中的code字段
                    # self.assertEqual(res['code'],0)



if __name__ == '__main__':
    # unittest.main()
    report_path = REPORT_PATH + '\\api_report.html'
    with open(report_path,'wb') as f:
        runner = HTMLTestRunner(stream=f,      #报告路径
                                verbosity=2,
                                title='API测试报告',   #报告标题
                                description='接口html测试报告',   #描述可不写
                                tester='小黑')   #测试人
        runner.run(TestUserAPI('test_login_01'))     #添加用例类里面的用例方法
    #发送邮件
    # e = Email(server='smtp.qq.com',
    #               sender='2538778461@qq.com',
    #               password='efvczhscfbhzdjia',
    #               receiver='aa2538778461@163.com',
    #               title='API自动化测试报告',
    #               path=report_path)
    # e.send()