# -*- coding: utf-8 -*-
'''
Created on 2019年5月25日
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
from bs4 import BeautifulSoup#引入beautifulsoup加快解析速度
from selenium import  webdriver
import time
import re
from pymongo import MongoClient
from io import StringIO
import os

# def crawl_articles_detail(driver,collection,lanmu):
        
if __name__ == '__main__':
    mongo_con=MongoClient('localhost', 27017)
    db=mongo_con.University
    collection=db.university_department_dir
    university_page=[i for i in range(20,861,20)]
    options = webdriver.ChromeOptions() 
    prefs = {'download.default_directory': 'G:/articles/',"download.prompt_for_download": False}
    options.add_experimental_option('prefs', prefs) 
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    for i in university_page:
        driver.get('https://yz.chsi.com.cn/sch/?start='+str(i))#打开网站
        content1=driver.page_source.encode('utf-8')
        soup1= BeautifulSoup(content1, 'lxml')#文章内容
        univer_tr=soup1.find(class_="ch-table").find('tbody').findAll('tr')#每一页的大学信息
        print(len(univer_tr))
        for j in univer_tr:
            univer_td=j.findAll('td')
        #     print(univer_tr)
            univer_name=univer_td[0].text.strip()#大学名字
            univer_url='https://yz.chsi.com.cn'+(univer_td[0].a['href'])#大学链接
            univer_location=univer_td[1].text#大学所在地
            univer_Subordinate_department=univer_td[2].text#院校隶属
            print(j.findAll(class_='ch-table-tag'))
            if j.findAll(class_='ch-table-tag'):
                if(j.findAll(class_='ch-table-tag')[0].text.strip())=='985':
                   univer_tag='985'
                else:
                    univer_tag='211'
            else:
                univer_tag='无'
            print(univer_url,univer_tag)
            driver.get(univer_url)#打开登陆网站
            content2=driver.page_source.encode('utf-8')
            soup2= BeautifulSoup(content2, 'lxml')#院校详细信息页面
            department_url='https://yz.chsi.com.cn'+soup2.find(class_='yxk-content').findAll('li')[1].a['href']#院系链接
            driver.get(department_url)#打开院系设置页面
            content3=driver.page_source.encode('utf-8')
            soup3= BeautifulSoup(content3, 'lxml')#院校详细信息页面
            if soup3.find(class_='yxk-content').findAll('a'):
                all_department=soup3.find(class_='yxk-content').findAll('a')#所有系
                for k in all_department:
#                     print(k)
                    try:
                        department_Url=k['href']#院系链接
                    except KeyError:
                        department_Url='暂无'
                    print(k.text)
#                     pattern=re.compile('>(.*)</span>')
                    department_name=k.text.strip()#院系名
                    print(department_name)
                    collection.insert({'University_name':univer_name,'University_detail_url':univer_url,'University_location':univer_location,\
                                      'University_Subordinate_department':univer_Subordinate_department,'univer_tag':univer_tag,'department_Url':department_Url,\
                                      'department_name':department_name
                                      })
            else:
                department_Url='暂无'
                department_name='暂无'
                collection.insert({'University_name':univer_name,'University_detail_url':univer_url,'University_location':univer_location,\
                                      'University_Subordinate_department':univer_Subordinate_department,'univer_tag':univer_tag,'department_Url':department_Url,\
                                      'department_name':department_name
                                      })
    mongo_con.close()
    driver.quit()