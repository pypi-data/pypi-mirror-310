#! /usr/bin/env python
'''
Auther      : xiaobaiTser
Email       : 807447312@qq.com
createTime  : 2024/11/21 1:09
fileName    : CSV.py
'''
import os.path
from csv import reader, writer

def Reader(file_path: str, ignore_first_row: bool = True):
    return list(reader(open(file_path, 'r', encoding='utf-8')))[1:] if ignore_first_row else \
        list(reader(open(file_path, 'r', encoding='utf-8')))

def Writer(file_path: str = '', data: list[list] = None, ignore_first_row: bool = False):
    data = data[1:] if ignore_first_row else data
    mode = 'a' if ignore_first_row else 'w'
    writer(open(file_path, mode, encoding='utf-8', newline='')).writerows(data)
    print(f'[{os.path.realpath(file_path)}] 写入 {data} 成功')



# if __name__ == '__main__':
#     Writer(file_path='../case_data_file/接口名称.csv',
#            data=[
#              ['method', 'uri', 'headers', 'data'],
#              ['GET', '/login', {'content-type': 'application/json'}, {'id':5}]
#            ],
#            ignore_first_row=True)

    # print(Reader(file_path='../case_data_files/api.csv', ignore_first_row=True))