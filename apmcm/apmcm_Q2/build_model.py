# -*- coding: utf-8 -*-
'''
Created on 2018年11月24日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import pandas as pd
import sklearn as sk
import numpy as np
import math
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error   #均方误差回归损失
from sklearn.cross_validation import train_test_split
from sklearn.model_selection import cross_val_score
# dataset=pd.read_csv(r'./data4.csv')#先用时间序列自回归预测未来三年国民生产总值，第一产业，第二产业，和第三产业
# print(dataset.columns.values.tolist())
# dataset=dataset.drop(columns=['第三产业','第二产业','国内生产总值','Sector'])
# label=dataset['第一产业']#预测第一产业
# dataset=dataset.drop(columns=['第一产业'])
# print(dataset.columns.values.tolist())
# dataset=dataset.astype(int)
# x_train,x_test,y_train,y_test=train_test_split(dataset,label,random_state=1)
# print(len(x_train),len(y_train))
# from sklearn.linear_model import LinearRegression#线性回归
# slr = LinearRegression()
# slr.fit(x_train, y_train)
# scores=cross_val_score(slr,x_test,y_test,cv=5)#[ 0.89949469  0.78829932  0.97473568  0.91050122  0.92494658]
# print(scores)
# print(slr.coef_)
# print(slr.intercept_)
# y_train_pred = slr.predict(x_train)
# y_test_pred =slr.predict(x_test)
# print('MSE train: %.3f, test: %.3f' % (mean_squared_error(y_train, y_train_pred),mean_squared_error(y_test, y_test_pred)))
# print('R^2 train: %.3f, test: %.3f' % (r2_score(y_train, y_train_pred),r2_score(y_test, y_test_pred)))#Output:#MSE train: 1.642, test: 11.052#R^2 train: 0.979, test: 0.878
# plt.scatter(y_train_pred, y_train_pred - y_train, c='black', marker='o', s=35, alpha=0.5, label='Training data')
# plt.scatter(y_test_pred, y_test_pred - y_test, c='lightgreen', marker='s', s=35, alpha=0.7, label='Test data')
# plt.xlabel('Predicted values')
# plt.ylabel('Residuals')
# plt.legend(loc='upper left')
# plt.hlines(y=0, xmin=-10, xmax=50, lw=2, color='red')
# plt.xlim([-10, 50])
# plt.tight_layout()
# # plt.savefig('./figures/slr_residuals.png', dpi=300)
# plt.show()
dataset=pd.read_csv(r'./data6.csv')#先用时间序列自回归预测未来三年国民生产总值，第一产业，第二产业，和第三产业
print(dataset.columns.values.tolist())
dataset=dataset.drop(columns=['本科以上'])
Sector=dataset['Sector'].dropna().unique()
print(Sector)
dataset=pd.get_dummies(dataset,columns=['Sector'])
label=dataset['Total demands']#预测第一产业
dataset=dataset.drop(columns=['本科以下','Unlimited','month','Total demands'])
print(dataset.columns.values.tolist())
dataset=dataset.astype(int)
x_train,x_test,y_train,y_test=train_test_split(dataset,label,random_state=1)
print(len(x_train),len(y_train))
from sklearn.linear_model import LinearRegression#线性回归
slr = LinearRegression()
slr.fit(x_train, y_train)
scores=cross_val_score(slr,x_test,y_test,cv=5)#[ 0.89949469  0.78829932  0.97473568  0.91050122  0.92494658]
print(scores)
print(slr.coef_)
print(slr.intercept_)
y_train_pred = slr.predict(x_train)
y_test_pred =slr.predict(x_test)
print('MSE train: %.3f, test: %.3f' % (mean_squared_error(y_train, y_train_pred),mean_squared_error(y_test, y_test_pred)))
print('R^2 train: %.3f, test: %.3f' % (r2_score(y_train, y_train_pred),r2_score(y_test, y_test_pred)))#Output:#MSE train: 1.642, test: 11.052#R^2 train: 0.979, test: 0.878
plt.scatter(y_train_pred, y_train_pred - y_train, c='black', marker='o', s=35, alpha=0.5, label='Training data')
plt.scatter(y_test_pred, y_test_pred - y_test, c='lightgreen', marker='s', s=35, alpha=0.7, label='Test data')
plt.xlabel('Predicted values')
plt.ylabel('Residuals')
plt.legend(loc='upper left')
plt.hlines(y=0, xmin=-10, xmax=50, lw=2, color='red')
plt.xlim([-10, 50])
plt.tight_layout()
# plt.savefig('./figures/slr_residuals.png', dpi=300)
plt.show()

validate=pd.DataFrame(columns=['Sector','total_monthes'])
sector=[]
total_monthes=[]
for i in range(37,73):
    for j in Sector:
        sector.append(j)
        total_monthes.append(i)
validate['Sector']=sector
validate['total_monthes']=total_monthes
print(validate)
validate_SET=pd.get_dummies(validate,columns=['Sector'])
y_VALI_pred =slr.predict(validate_SET)
validate['total_demand']=np.abs(np.round(y_VALI_pred))
validate.to_csv('./validate.csv')

    




    