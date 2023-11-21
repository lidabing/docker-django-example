from __future__ import absolute_import, unicode_literals
from celery import shared_task
import os
import redis
import requests 
import json



def read_cookie_from_file(file_path):
    """
    从文件中读取cookie。

    参数:
        file_path: cookie文件的路径。

    返回:
        文件的内容。
    """
    with open(file_path, 'r') as f:
        return f.read()

def get_bonds_data(url, referer):
    cookie_file = os.path.dirname(os.path.realpath(__file__)) +"/cookie.txt"
    cookie = read_cookie_from_file(cookie_file)  
    headers = {
        'Referer': referer,
        'cookie': cookie,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en,zh-CN;q=0.9,zh;q=0.8,zh-HK;q=0.7,zh-TW;q=0.6,ko;q=0.5',
        'Dnt':'1',
        'If-Modified-Since':'Mon, 04 Sep 2023 11:10:38 GMT',
        'Init':'1',
        'Sec-Ch-Ua':'"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'Sec-Ch-Ua-Mobile':'?1',
        'Sec-Ch-Ua-Platform':"Android",
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    return response

@shared_task
def my_task():
    print("This is a task.")
    
    
@shared_task
def download_and_save_data():
    # url = "https://www.jisilu.cn/webapi/cb/list/"
    # referer = 'https://www.jisilu.cn/web/data/cb/list'
    # response =get_bonds_data(url,referer)
    # data = response.json()  # Or response.json(), response.content, etc., depending on the data format
    # r = redis.Redis(host='convertible_bond-redis-1', port=6379, db=0)
    # data_str = json.dumps(data)  # Convert the dict to a string
    # r.set('downloaded_data', data_str)
    print('download_and_save_data')