#! /usr/bin/env python
'''
Auther      : xiaobaiTser
Email       : 807447312@qq.com
createTime  : 2024/11/21 14:48
fileName    : email_config.py
'''

from ..common.Network import get_ip, get_local_ip
from ..config.allure_config import Allure

class EMail(object):
    # QQ的SMTP服务域名
    _QQ_SMTP_HOST_      : str = 'smtp.qq.com'
    _163_SMTP_HOST_     : str = 'smtp.163.com'
    # SMTP服务域名或者IP
    SMTP_HOST           : str = _163_SMTP_HOST_
    # SMTP端口号
    SMTP_PORT           : int = 465
    # 邮箱登录用户名
    SMTP_UserName       : str = ''
    # 邮箱密码或者授权码
    SMTP_Passwd         : str = ''
    # 邮件标题
    Subject_Title       : str = '自动化测试'
    # 收件人
    Receiver            : list|str = None

    Content_HTML        : str = f'''
<html>
    <body>
        <h2>测试结果的查看</h2>
        <div id="report">
            <span id="1">
                <a href="http://{get_local_ip()}:{Allure.PORT}">访问局域网Allure报告</a><br>
                <a href="http://{get_ip()}:{Allure.PORT}">访问公网Allure报告</a>
            </span>
            <span id="2">
                <b>下载查看附件，pytest的简单报告<b>
            </span>
        </div>
    <body>
</html>
    '''