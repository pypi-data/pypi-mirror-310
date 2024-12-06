#! /usr/bin/env python
'''
Auther      : xiaobaiTser
Email       : 807447312@qq.com
createTime  : 2024/11/18 23:28
fileName    : run_main.py
'''
import os
import pytest
from api_project.common import init
from api_project.config.host_config import HOST

if __name__ == '__main__':
    # HOST.CURRENT_HOST = ''  # 提示：提前设置域名或者在配置文件中配置

    init()    # 初始化数据，加载环境变量，例如：清空工作文件夹或文件，设置HOST地址

    # 执行用例
    pytest.main([
        'api_project/case_scripts',
        '-q',
        '-s',
        '--alluredir=api_project/data',
        '--html=api_project/report/report.html',
        '--self-contained-html'
    ])

    # 生成 Allure 报告
    os.popen('allure serve api_project/data')

    # 发邮件
