# -*- coding: utf-8 -*-
'''
Created on 2019年4月18日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import numpy as np
u=np.mat([1,2,0,0,3,0,0,0,4,0])
mu=u.T
list=[]
for i in range(0,10):
    for j in range(0,10):
        c=0.8**abs(i-j)
        list.append(c)
co=np.array(list)
# co.shape=(10,10)
cov=np.transpose(co)
print(cov)
x=np.random.normal((10,1))
print(x)