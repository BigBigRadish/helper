# -*- coding: utf-8 -*-
'''
Created on 2019年4月22日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import math
def Re_cosi_dev_D(Re,cosi_dev):
    i=1
    j=0.0
    while(i!=0):
        j+=0.0001
        if(-0.0001<=1.0/math.sqrt(j)-1.74+2*(math.log10((2*cosi_dev)+(18.7/Re*math.sqrt(j))))<=0.0001):
            i=0
            print(j)
j=Re_cosi_dev_D(10, 5) 
          
        
    