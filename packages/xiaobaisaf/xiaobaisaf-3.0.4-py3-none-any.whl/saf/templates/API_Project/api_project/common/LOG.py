#! /usr/bin/env python
'''
Auther      : xiaobaiTser
Email       : 807447312@qq.com
createTime  : 2024/11/23 22:30
fileName    : LOG.py
'''
import os
from datetime import datetime
from .. import LOG_DIR_PATH

class Logger(object):
    def __init__(self, logfile: str = None):
        self.logfile = os.path.join(LOG_DIR_PATH, logfile)

    def logging(self, message, level) -> str:
        if level.lower() in ['debug', 'info', 'warning', 'error']:
            log = [
                f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]',
                ' - ',
                f'[{level.upper()}]',
                ' - ',
                f'{message}',
                f'\n'
            ]
            log_content =  ''.join(log)
            if self.logfile:
                with open(self.logfile, 'a') as f:
                    f.write(log_content + '\n')
                    f.close()
            return log_content
        else:
            raise ValueError(f"无效的日志level: {level}, 有效level范围是：'debug', 'info', 'warning', 'error'")

    def info(self, message: str = '') -> str:
        return self.logging(message, level='INFO')

    def error(self, message: str = '') -> str:
        return self.logging(message, level='ERROR')

    def warning(self, message: str = '') -> str:
        return self.logging(message, level='WARNING')

    def debug(self, message: str = '') -> str:
        return self.logging(message, level='DEBUG')
