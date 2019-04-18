# -*- coding: utf-8 -*-
'''
Created on 2019年4月18日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import numpy as np
u=[1,2,0,0,3,0,0,0,4,0]
# mu=u.T
list=[]
for i in range(0,10):
    for j in range(0,10):
        c=0.8**abs(i-j)
        list.append(c)
# co.shape=(10,10)
a=np.random.normal(u[0],list[0],(1,1000))+np.random.normal(0,0.1,(1,1000))
for i in range(1,10):
    b1=np.random.normal(u[i],list[i],(1,1000))+np.random.normal(0,0.1,(1,1000))
    a=np.vstack((a,b1))                                                       
cov=np.transpose(a)
print(cov)
print(cov.shape)