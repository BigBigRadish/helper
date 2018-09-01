# -*- coding: utf-8 -*-
'''
Created on 2018年10月6日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import pandas as pd 
data_file='E:\workplace\helper\mengyuan_titanic\MD.xls'
# train=pd.read_csv('./train.csv')
# print('含有缺失值的行数'+'\n'+str(train.isnull().sum()))#输出缺失值
import win32com.client
excel = win32com.client.Dispatch('Excel.Application')
workbook = excel.Workbooks.open(data_file)
sheet = workbook.WorkSheets('sheet name')
## get the cell value
row,col = 1,1
print(sheet.Cells(row,col).value)