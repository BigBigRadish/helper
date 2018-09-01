# -*- coding: utf-8 -*-
'''
Created on 2018年11月24日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import pandas as pd
import xlrd
import os
import scipy
def merge_data():#数据合并
    #text=pd.read_excel('./2018_APMCM_Problem_B/Annex_Job_market_of_A_City_Market_Demand_Statistics/2015/09.xlsx')
#     year=['2015']
#     month=['09','10','11','12',]
#     for year1 in year:
#             for month1 in month:
#      text1=pd.read_excel('2018_APMCM_Problem_B/Annex_Job_market_of_A_City_Market_Demand_Statistics/2011.01.01-2012.12.14.xls')
#      text1.to_csv('2018_APMCM_Problem_B/Annex_Job_market_of_A_City_Market_Demand_Statistics/2011.01.01-2012.12.14.csv')  
    year=['2015','2016','2017','2018']
    f=open('/合并数据集', mode='a', encoding='utf-8')
    j=0
    for year1 in year:
        path = r'E:/workplace/helper/apmcm/2018_APMCM_Problem_B/Annex_Job_market_of_A_City_Market_Demand_Statistics/'+year1
        files = os.listdir(path)
        for i in files:
            j+=1
            pathname=path+'/'+i
            file=pd.read_csv(pathname)
            #print(file)
            file['year']=[year1 for _ in range(0,len(file['s/n']))]
            file['month']=[i.replace('.csv','') for _ in range(0,len(file['s/n']))]
            file['total_monthes']=[j for _ in range(0,len(file['s/n']))]
            file.to_csv('./合并数据集.csv', sep=',', mode='a', encoding='utf-8')
if __name__ == '__main__':
    dataset=pd.read_csv('./合并数据集.csv')
    