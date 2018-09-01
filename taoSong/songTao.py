# -*- coding: utf-8 -*-
'''
Created on 2019年01月13日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
'''
涛哥遗传算法模型值的预测
'''
import pandas as pd
import numpy as np
import matplotlib as mlp
import matplotlib.pyplot as plt
import seaborn as sns
import warnings; warnings.filterwarnings(action='once')

import math
from sklearn import tree
from sklearn.cross_validation import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error   #均方误差回归损失
# 导入数据集
df = pd.read_csv("./data/taoSong.csv")
df_1=df[df.label.notnull()].astype("float")#训练集
print(df_1)
df_2=df[df.label.isnull()].drop(columns=['label']).astype("float")
print(df_2)
# # 绘制热点图
# plt.figure(figsize=(12,10), dpi= 80)
# sns.heatmap(df.corr(), xticklabels=df.corr().columns, yticklabels=df.corr().columns, cmap='RdYlGn', center=0, annot=True)
# #组装
# plt.title('Correlogram of mtcars', fontsize=22)
# plt.xticks(fontsize=12)
# plt.yticks(fontsize=12)
# plt.show()
label=df_1['label']
feature_set=df_1.drop(columns=['label'])
x_train,x_test,y_train,y_test=train_test_split(feature_set,label,random_state=1)

clf=tree.DecisionTreeRegressor()#决策树回归模型
clf=clf.fit(x_train,y_train)
'''
决策树回归
score:[-0.33892617 -0.0802063  -0.08821056 -0.17430894 -0.23557537]
MSE train: 0.000, test: 24.859
R^2 train: 1.000, test: 0.023
'''

feature_name=feature_set.columns.values.tolist()
y_importances=clf.feature_importances_
print(y_importances)
x_importances=feature_name
y_pos=np.arange(len(x_importances))
#横向柱状图
plt.barh(y_pos,y_importances,align='center')
plt.yticks(y_pos,x_importances)
plt.xlabel('importances')
plt.xlim(0,1)
plt.title('feature importance')
plt.show()
plt.savefig('clf_feature_importance')#特征重要度

scores=cross_val_score(clf,x_test,y_test,cv=5)
print(scores)
y_train_pred = clf.predict(x_train)
y_test_pred =clf.predict(x_test)
print('MSE train: %.3f, test: %.3f' % (mean_squared_error(y_train, y_train_pred),mean_squared_error(y_test, y_test_pred)))
print('R^2 train: %.3f, test: %.3f' % (r2_score(y_train, y_train_pred),r2_score(y_test, y_test_pred)))
plt.scatter(y_train_pred, y_train_pred - y_train, c='black', marker='o', s=35, alpha=0.5, label='Training data')
plt.scatter(y_test_pred, y_test_pred - y_test, c='lightgreen', marker='s', s=35, alpha=0.7, label='Test data')
plt.xlabel('Predicted values')
plt.ylabel('Residuals')
plt.legend(loc='upper left')
plt.hlines(y=0, xmin=-10, xmax=50, lw=2, color='red')
plt.xlim([-10, 50])
plt.tight_layout()
plt.savefig('./data/clf_residuals.png', dpi=300)

#预测

y_predict=clf.predict(df_2)
df_2['dwell']=y_predict
df_2.to_csv('./data/pre_clf_data.csv')#