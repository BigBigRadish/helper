# -*- coding: utf-8 -*-
'''
Created on 2019年5月28日
@author: Zhukun Luo
Jiangxi university of finance and economics
'''

'''
Goals:
 1. Collect information on department chairs and department party secretaries (name, year of service, CV) for social sciences departments (e.g. Economics, Political Science). 
     a. Please randomly pick 1 department from a 985 university and 1 department from a university not in the 985/211 rank. 
     b. Timeframe: focus on year 2000 to today.
 2. Use sources such as CNKI, Google Scholar, and Baidu Baike to collect information on all the papers published by all researchers (including dean/chair) from these departments during this time frame. 
 3. Identify patterns of published research during this time, and the relationship of published research by department members and the leaders. 
'''
import requests
from bs4 import BeautifulSoup#引入beautifulsoup加快解析速度
import time
import re
from pymongo import MongoClient
from io import StringIO
import os
import pandas as pd
# options = webdriver.ChromeOptions() 
# prefs = {'download.default_directory': 'G:/articles/',"download.prompt_for_download": False}
# options.add_experimental_option('prefs', prefs) 
# driver = webdriver.Chrome(chrome_options=options)
# driver.maximize_window()
headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'Host':
            'kns.cnki.net',
            'Connection':
            'keep-alive',
            'Cache-Control':
            'max-age=0',
        }
def crawl_paper_by_cnki(collection,university,name,topic):#search paper infor by university,name,research area
    cnki_url='http://kns.cnki.net/kns/brief/result.aspx?dbprefix=SCDB&crossDbcodes=CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD'#高级检索
#     driver.get(cnki_url)
    # 利用post请求先行注册一次
    SEARCH_HANDLE_URL = 'http://kns.cnki.net/kns/request/SearchHandler.ashx'
    # 发送get请求获得文献资源
    GET_PAGE_URL = 'http://kns.cnki.net/kns/brief/brief.aspx?pagename='
    session = requests.Session()
    session.get(cnki_url)
    static_post_data = {
            'action': '',
            'NaviCode': '*',
            'ua': '1.21',
            'isinEn': '1',
            'PageName': 'ASP.brief_default_result_aspx',
            'DbPrefix': 'SCDB',
            'DbCatalog': '中国学术期刊网络出版总库',\
            'ConfigFile': 'SCDB.xml',\
            'db_opt': 'CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',  # 搜索类别（CNKI右侧的）
            'publishdate_from':'2000-01-01',
            'txt_2_sel':'SU$%=|',
            'txt_2_value1':topic,
            'txt_2_logical':'and',
            'txt_2_relation':'#CNKI_AND',
            'txt_2_special1':'=',
            'au_1_sel':'AU',
            'au_1_sel2':'AF',
            'au_1_value1':name,
            'au_1_value2':university,
            'au_1_special1':'=',
            'au_1_special2':'%',
            'db_value': '中国学术期刊网络出版总库',\
            'year_type': 'echar',\
            'his': '0',\
            'db_cjfqview': '中国学术期刊网络出版总库,WWJD',\
            'db_cflqview': '中国学术期刊网络出版总库',\
            '__': time.asctime(time.localtime()) + ' GMT+0800 (中国标准时间)'}# 将固定字段与自定义字段组合
    post_data = {**static_post_data}
    # 必须有第一次请求，否则会提示服务器没有用户
    first_post_res = session.post(
            SEARCH_HANDLE_URL, data=post_data, headers=headers)
    print(first_post_res.text)
    get_result_url = GET_PAGE_URL + first_post_res.text
    second_get_res = session.get(get_result_url, headers=headers)
#     print(second_get_res)
#     soup1= BeautifulSoup(second_get_res.content, 'lxml')#文章内容
#     print(soup1)
    #获取跳转链接
#     change_page_pattern_compile = re.compile(
#             r'.*?pagerTitleCell.*?<a href="(.*?)".*')
#     change_page_url = re.search(change_page_pattern_compile,
#                                          second_get_res.text).group(1)
#     print(change_page_url)
    #获取总页数
    reference_num_pattern_compile = re.compile(r'.*?找到&nbsp;(.*?)&nbsp;')
    reference_num = re.search(reference_num_pattern_compile,\
                              second_get_res.text).group(1)
    reference_num_int = int(reference_num.replace(',', ''))
    print(reference_num)
    for k in range(1,reference_num_int):
        time.sleep(1)
        content_url='http://kns.cnki.net/kns/brief/brief.aspx?curpage='+str(k)+'&RecordsPerPage=20&QueryID=0&ID=&turnpage=1&tpagemode=L&dbPrefix=SCDB&Fields=&DisplayMode=listmode&PageName=ASP.brief_result_aspx&isinEn=1&'
        page_content=session.get(content_url, headers=headers)
        time.sleep(1)
        soup = BeautifulSoup(page_content.text, 'lxml')
    #     print(soup)
        # 定位到内容表区域
        tr_table = soup.find(name='table', attrs={'class': 'GridTableContent'})
        if tr_table.tr.string !=None:
            tr_table.tr.extract()
        #     print(tr_table)
            for i in tr_table.findAll('tr'):#每一个文献块
                paper_detail=i.findAll('td')
        #         print(paper_detail[1])
                paper_name=paper_detail[1].a.text#文章名
                paper_profile_url='http://kns.cnki.net'+paper_detail[1].a['href']#文章详情页面
                author_flags=[]#合作者名单及主页
                for j in paper_detail[2].findAll('a'):
                    author_flags.append({j.text:'http://kns.cnki.net'+j['href']})
                paper_origin=paper_detail[3].a.text#文章来源
                paper_origin_link='http://kns.cnki.net'+paper_detail[3].a['href']#文章来源链接
                paper_publish_time=paper_detail[4].text#文章发表时间
                paper_db_type=paper_detail[5].text#文章来源数据库类型
                paper_download_link='http://kns.cnki.net'+paper_detail[7].findAll('a')[0]['href']#文章下载链接
                if paper_detail[7].findAll('a')[1]:
                    paper_download_count=paper_detail[7].findAll('a')[1].text#文章下载次数
                else:
                    paper_download_count='0'
                print(paper_name,paper_download_count)
                paper_insert={'机构':university,'姓名':name,'关键词':topic,'文章名':paper_name,'文章详情页面':paper_profile_url,'合作者名单及主页':str(author_flags)\
                              ,'文章来源':paper_origin,'文章来源链接':paper_origin_link,'文章发表时间':paper_publish_time,'文章来源数据库类型':paper_db_type,\
                              '文章下载链接':paper_download_link,'文章下载次数':paper_download_count}
                collection.insert(paper_insert)
        else:
            break
            
        
if __name__ == '__main__':
    mongo_con=MongoClient('localhost', 27017)
    db=mongo_con.University
    collection=db.author_paper_detail
    peaking_univer_member=pd.read_csv('./peaking_economic_researcher_chinese_info.csv')['name'].values#北京大学人员名单
    BLCU_members=pd.read_csv('./BLCU_economic_researcher.csv')['name'].values#北京语言大学人员名单
    for member1 in peaking_univer_member:
        crawl_paper_by_cnki(collection,'北京大学经济学院',member1,'经济')
    for member2 in peaking_univer_member:
        crawl_paper_by_cnki(collection,'北京语言大学商学院',member2,'经济')
        