# -*- coding: utf-8 -*-
'''
Created on 2019年5月26日
@author: Zhukun Luo
Jiangxi university of finance and economics
'''

'''
Goals:
 1. Collect information on department chairs and department party secretaries (name, year of service, CV) for social sciences departments (e.g. Economics, Political Science). 
     a. Please randomly pick 1 department from a “985” university and 1 department from a university not in the 985/211 rank. 
     b. Timeframe: focus on year 2000 to today.
 2. Use sources such as CNKI, Google Scholar, and Baidu Baike to collect information on all the papers published by all researchers (including dean/chair) from these departments during this time frame. 
 3. Identify patterns of published research during this time, and the relationship of published research by department members and the leaders. 
'''
import pandas as pd
import re
from bs4 import BeautifulSoup
import requests
import random
from selenium import  webdriver
import pdfkit
user_agent = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
headers={'User-Agent':user_agent}
requests.adapters.DEFAULT_RETRIES = 5
university_department=pd.read_csv('./university_department.csv',encoding='utf-8')
university_985=university_department[university_department['univer_tag']=='985']['University_name'].drop_duplicates().reset_index()
university_choice_985=random.choice(university_985.values)
print(university_choice_985)#random choice 985->'北京大学'
university_not_985211=university_department[university_department['univer_tag']=='无']['University_name'].drop_duplicates().reset_index()
university_choice_not_985211=random.choice(university_not_985211.values)
print(university_choice_not_985211)#random choice not 985 and 211
'''
[0 '北京大学']
[157 '北京语言大学']
'''
peaking_univer=university_department[university_department['University_name']=='北京大学']
Beijing_la_cul_univer=university_department[university_department['University_name']=='北京语言大学']
print('peaking_univer:',peaking_univer['department_name'],'北京语言大学：',Beijing_la_cul_univer['department_name'])
'''
peaking_univer: 
0        教学单位详情
1           医学部
2        深圳研究生院
3        数学科学学院
4        生命科学学院
5     化学与分子工程学院
6       马克思主义学院
7        政府管理学院
8        国际关系学院
9      信息科学技术学院
10         经济学院
11       光华管理学院
12        外国语学院
13          法学院
14         教育学院
15         物理学院
16      新闻与传播学院
17     软件与微电子学院
18    地球与空间科学学院
19      城市与环境学院
20     对外汉语教育学院
21    环境科学与工程学院
22          工学院
23       考古文博学院
24         艺术学院
25    建筑与景观设计学院
26        体育教研部
27    心理与认知科学学院
28        信息管理系
29      中国语言文学系
30         历史学系
31    哲学系(宗教学系)
32         社会学系
33      国家发展研究院
34        人口研究所
35      分子医学研究所
36        歌剧研究院
37    前沿交叉学科研究院
38       新媒体研究院
39         燕京学堂
北京语言大学： 157    暂无
'''
'''
由于北京语言大学在研招网上没有具体院系信息，所以需要人工选择。这里我们选择经济相关的系,北大选择经济学院，北京语言大学选择商学院，分别爬取学院所有教职人员的发表论文信息
'''
'''
http://econ.pku.edu.cn/xyjj/xyjj3/index.htm->北大经济学院{院长:董志勇:{电话：010-62759760,邮箱：dzy@pku.edu.cn},党委书记:崔建华:{}}
'''
def get_cv(university_depart,name):#从百度百科得到简历
    html=requests.get('https://baike.baidu.com/search/none?word='+university_depart+name,headers=headers,verify=False)
    soup=BeautifulSoup(html.content,"lxml",from_encoding='utf-8')
    baidubaike_profile_url=soup.find(class_='search-list').find('dd').a['href']
    print(baidubaike_profile_url)
    pdfkit.from_url(baidubaike_profile_url,'./cv/'+university_depart+name+'.pdf')#方法一，含有广告
#     html1=requests.get(baidubaike_profile_url,headers=headers,verify=False)
#     soup1=BeautifulSoup(html1.content,"lxml",from_encoding='utf-8')
#     print(soup1.findAll('dl'))
#     pdfkit.from_url('https://baike.baidu.com/item/%E8%91%A3%E5%BF%97%E5%8B%87/4594858','./out.pdf') 
# get_cv('北京大学经济学院', '院长') 
# get_cv('北京大学经济学院', '党委书记') 
# get_cv('','杜金富')#百度百科 无此人信息
# get_cv('北京语言大学商学院', '党委书记')#百度百科 无此人信息
def get_researcher_from_peaking_university_chinese(url):#中文版信息页面
    html=requests.get(url,headers=headers,verify=False)
    soup=BeautifulSoup(html.content,"lxml",from_encoding='utf-8')
    person_detail=soup.findAll(class_='teacherone fl')
    for j in person_detail:
        name=j.find('h1').text
        for k in j.findAll('p'):
            print(k.text.strip())
            if '邮箱' in str(k.text):
                email=k.text.replace('邮箱：','')
        with open('./peaking_economic_research_list.csv','a',encoding='utf-8')as f:
            f.write(name+','+email+'\n')
def get_researcher_from_peaking_university_english(url):#english page
    html=requests.get(url,headers=headers,verify=False)
    soup=BeautifulSoup(html.content,"lxml",from_encoding='utf-8')
    deparents_faculty=soup.findAll(class_='right_c')
    for i in deparents_faculty:
        for j in i.findAll('div'):
            personal_profile_url='http://econ.pku.edu.cn/english/faculty/fulltimefaculty/'+j.find('a')['href']
            name=j.strong.text
            print(name,personal_profile_url)
#             pdfkit.from_url(personal_profile_url,'./cv/peaking_university_researcher_cv/'+name.strip()+'.pdf')#the cv of all researchers
            with open('./peaking_economic_researcher_english.csv','a',encoding='utf-8')as f:
                f.write(name+','+personal_profile_url+'\n')
# url='http://econ.pku.edu.cn/english/faculty/fulltimefaculty/index.htm'#英文主页
# get_researcher_from_peaking_university_english(url)
# title=['qzjs','bsh']#北大经济学院中文主页
# for i in title:
#     get_researcher_from_peaking_university_chinese(url='http://econ.pku.edu.cn/jsyyj/'+i+'/index.htm')
BACU_url=['http://bs.blcu.edu.cn/col/col2423/index.html?uid=7234&pageNum=1']
def get_researcher_from_BACU_chinese(url):#异步加载
#     print(html)
    html=requests.get(url,cookies=_cookies,headers=headers,verify=False)
    html.encoding='utf-8'
    pattern1=re.compile('cursor:hand\' href=\'(.*)\'   target')
    profile_urls=pattern1.findall(html.text)#所有的主页链接
    pattern2=re.compile('class=\'bt_link\' target=\'_blank\'>(.*)</a></br>')
    researcher_name=pattern2.findall(html.text)
    pattern3=re.compile('</a></br>(.*)</br></p>')
    researcher_title=pattern3.findall(html.text)
    print(profile_urls,researcher_name,researcher_title)
    for a,b,c in zip(profile_urls,researcher_name,researcher_title):
        pdfkit.from_url('http://bs.blcu.edu.cn'+a,'./cv/BLCU_economics_cv/'+b.strip()+'.pdf')#the cv of all blcu researchers
        with open('./BLCU_economic_researcher_english.csv','a',encoding='utf-8')as f:
                f.write(b+','+c+','+a+'\n')
# html1=requests.get('http://bs.blcu.edu.cn/module/visitcount/visit.jsp',headers=headers,verify=False)
# _cookies=html1.cookies   
# print(_cookies) 
# for i in BACU_url:  
#     get_researcher_from_BACU_chinese(i)
blcu=pd.read_csv('./BLCU_economic_researcher.csv')
for index,i in blcu.iterrows():
    pdfkit.from_url('http://bs.blcu.edu.cn'+i['profile_url'],'./cv/BLCU_economics_cv/'+i['name']+'.pdf')
    

