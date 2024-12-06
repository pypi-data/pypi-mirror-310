#! /usr/bin/env python
'''
Auther      : xiaobaiTser
Email       : 807447312@qq.com
createTime  : 2024/11/21 0:44
fileName    : add_apis.py
'''

'''
cURL2apis
有curl脚本转为接口脚本
curl字符串：
    1、第一步转为python的request对象
    2、将对象按照模板生成脚本与数据文件
        config/case_config.py
        case_scripts/test_接口名称(小写).py
        case_data_files/接口名称(大写).csv
'''
import os
from urllib.parse import urlparse
from api_project.common.ENV import ENV
from api_project.common.CSV import Writer
from api_project import CASE_CONFIG_PATH, CASE_SCRIPT_DIR_PATH, CASE_DATA_DIR_PATH, FEED
from saf.utils.Curl2Object import Curl, Template


def add_apis(file_path: str = None):
    # 加载环境变量
    ENV.load()
    if file_path:
        # 加载环境变量
        ENV.load()
        # file = 'C:\\Users\\Administrator\\Desktop\\GET.bat'
        curl = Curl()
        curl.load(curl_file_path=file_path)

        for request in curl.group:
            # 获取接口名称：
            if 'API_COUNT' not in os.environ.keys():
                os.environ['API_COUNT'] = str(0)
            else:
                os.environ['API_COUNT'] = str(int(os.environ.get('API_COUNT')) + 1)
            _API_NAME_ = urlparse(request.get('url')).path.split('/')[-1]
            API_NAME = _API_NAME_.upper() if _API_NAME_ != '' else f"API_{os.environ.get('API_COUNT')}"
            try:
                newline = f"{API_NAME}_CASE_DATA_PATH = os.path.join(CASE_DATA_DIR_PATH, '{API_NAME}.csv'){FEED}"
                with open(CASE_CONFIG_PATH, 'r', encoding='utf-8') as fr:
                    alllines = fr.readlines()
                    if newline not in alllines:
                        # 写入测试用例数据路径
                        with open(CASE_CONFIG_PATH, 'a', encoding='utf-8') as fa:
                            fa.write(f"{newline}")
                            fa.close()
                        print(f"{CASE_CONFIG_PATH} 写入成功！")
                    del alllines
                    fr.close()
            except Exception as e:
                print(f"{CASE_CONFIG_PATH} 写入失败！{e}")

            # 写入测试用例脚本
            CASE_SCRIPT = os.path.join(CASE_SCRIPT_DIR_PATH, f"test_{API_NAME.lower()}.py")
            try:
                with open(CASE_SCRIPT, 'w', encoding='utf-8') as fw:
                    fw.write(Template.requests_pytest_allure_template(request=request))
                    fw.close()
                print(f"{CASE_SCRIPT} 写入成功！")
            except Exception as e:
                print(f"{CASE_SCRIPT} 写入失败！{e}")

            # 写入测试用例数据文件
            CASE_DATA = os.path.join(CASE_DATA_DIR_PATH, f"{API_NAME}.csv")
            Writer(file_path=CASE_DATA, data=[list(request.keys()),list(request.values())], ignore_first_row=False)