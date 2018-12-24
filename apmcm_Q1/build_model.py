# -*- coding: utf-8 -*-
'''
Created on 2018年11月24日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import pandas as pd
import sklearn as sk
import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn.model_selection import cross_val_score
dataset=pd.read_csv(r'./data.csv')
#print(dataset.columns.values.tolist())
print(dataset.columns.values.tolist())
dataset=pd.get_dummies(dataset,columns=['Sector','season','month','year'])
#print(dataset.columns.values.tolist())
dataset=dataset.astype(float)
#dataset.to_csv('./dataset.csv')
from sklearn import tree
from sklearn.cross_validation import train_test_split
feature_set=dataset.drop(columns=['Total demands'])
feature_name=feature_set.columns.values.tolist()
print(feature_name)
label=dataset['Total demands']
x_train,x_test,y_train,y_test=train_test_split(feature_set,label,random_state=1)
print(len(x_train),len(y_train))
# clf=tree.DecisionTreeRegressor()#决策树回归模型
# clf=clf.fit(x_train,y_train)
# scores=cross_val_score(clf,x_test,y_test,cv=5)#[ 0.73691812  0.79336203  0.91580625  0.78710664  0.77696305]
# print(scores)
# y_importances=clf.feature_importances_
# print(y_importances)
# x_importances=feature_name
# y_pos=np.arange(len(x_importances))
# #横向柱状图
# plt.barh(y_pos,y_importances,align='center')
# plt.yticks(y_pos,x_importances)
# plt.xlabel('importances')
# plt.xlim(0,1)
# plt.title('feature importance')
# plt.show()
import matplotlib.pyplot as plt 
import seaborn as sns
sns.set(style='whitegrid', context='notebook')   #style控制默认样式,context控制着默认的画幅大小
# cols = ['LSTAT', 'INDUS', 'NOX', 'RM', 'MEDV']
# sns.pairplot(dataset, size=2.5)
# plt.tight_layout()# plt.savefig('./figures/scatter.png', dpi=300)
# plt.show()
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error   #均方误差回归损失
import numpy as np
# cm = np.corrcoef(dataset.values.T)   #corrcoef方法按行计算皮尔逊相关系数,cm是对称矩阵#使用np.corrcoef(a)可计算行与行之间的相关系数,np.corrcoef(a,rowvar=0)用于计算各列之间的相关系数,输出为相关系数矩阵。
# sns.set(font_scale=1.5)   #font_scale设置字体大小
# hm = sns.heatmap(cm,cbar=True,annot=True,square=True,fmt='.2f',annot_kws={'size': 15},yticklabels=cols,xticklabels=cols)
# # plt.tight_layout()
# # plt.savefig('./figures/corr_mat.png', dpi=300)
# plt.show()
# def lin_regplot(X, y, model):
#     plt.scatter(X, y, c='lightblue')
#     plt.plot(X, model.predict(X), color='red', linewidth=2)    
#     return 
from sklearn.linear_model import LinearRegression#线性回归
slr = LinearRegression()
slr.fit(x_train, y_train)
scores=cross_val_score(slr,x_test,y_test,cv=5)#[ 0.89949469  0.78829932  0.97473568  0.91050122  0.92494658]
print(scores)
print(slr.coef_)
print(slr.intercept_)
# y_train_pred=np.round(slr.predict(x_train))
# y_test_pred =np.round(slr.predict(x_test))#MSE train: 126230.541, test: 323333.521 R^2 train: 0.917, test: 0.928
# print('MSE train: %.3f, test: %.3f' % (mean_squared_error(y_train, y_train_pred),mean_squared_error(y_test, y_test_pred)))
from sklearn.ensemble import RandomForestRegressor#随机森林回归
forest = RandomForestRegressor(n_estimators=1000, criterion='mse', random_state=1, n_jobs=-1)
forest.fit(x_train, y_train)#MSE train: 21123.455, test: 842033.039
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
scores=cross_val_score(forest,x_test,y_test,cv=5)#[ 0.83562915  0.785802    0.82791966  0.92894881  0.85761469]
print(scores)
y_test_pred = np.round(forest.predict(x_test))#MSE train: 21123.455, test: 842033.039 R^2 train: 0.986, test: 0.812
# print('MSE train: %.3f, test: %.3f' % (mean_squared_error(y_train, y_train_pred),mean_squared_error(y_test, y_test_pred)))
# print('R^2 train: %.3f, test: %.3f' % (r2_score(y_train, y_train_pred),r2_score(y_test, y_test_pred)))#Output:#MSE train: 1.642, test: 11.052#R^2 train: 0.979, test: 0.878plt.scatter(y_train_pred, y_train_pred - y_train, c='black', marker='o', s=35, alpha=0.5, label='Training data')plt.scatter(y_test_pred, y_test_pred - y_test, c='lightgreen', marker='s', s=35, alpha=0.7, label='Test data')plt.xlabel('Predicted values')plt.ylabel('Residuals')plt.legend(loc='upper left')plt.hlines(y=0, xmin=-10, xmax=50, lw=2, color='red')plt.xlim([-10, 50])plt.tight_layout()# plt.savefig('./figures/slr_residuals.png', dpi=300)plt.show()
# from sklearn.svm import SVR#效果极差MSE train: 1603158.384, test: 4795321.793 R^2 train: -0.054, test: -0.071
# svr = SVR(kernel = 'rbf')
# svr.fit(x_train, y_train)
# y_train_pred = svr.predict(x_train)
# y_test_pred = svr.predict(x_test)
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


    