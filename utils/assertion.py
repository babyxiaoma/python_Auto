'''
各种断言方法写在此处
'''

def assertHTTPCode(response,code_list=None):
    '''
    针对公司项目接口返回的code获取
    :param response: 传入response必须为json
    :param code_list:响应code_list,默认不传为0
    :return:
    '''
    res_code = response['code']
    if not code_list:
        code_list = [0]
    if res_code not in code_list:
        raise AssertionError('响应code值不在列表中!,实际响应code:%s,实际响应:%s' % (res_code,response))