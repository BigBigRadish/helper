# -*- coding: utf-8 -*-
'''
Created on 2019年5月16日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
raw_path='../Youku_00000_l/'
for i in range(1,101):
    path=raw_path+str(i)+'.png'
    with open(path,'rb') as f1:
        print(path)
#         print(f1.read())
    
