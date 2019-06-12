# -*- coding: utf-8 -*-
'''
Created on 2019年6月12日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import requests
import json
if __name__ == '__main__':
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
    headers={'User-Agent':user_agent}
    response=requests.get('http://api.so.eastmoney.com/bussiness/Web/getgubasearchList?type=8&pageindex=2&pagesize=90&keyword=st&name=normal&isAssociation=false',headers)
    print(json.loads(response.text))