# -*- coding: utf-8 -*-
'''
Created on 2018年12月16日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
quarter_log=pd.read_csv('./quarter_log.csv')
print(quarter_log)
ex=quarter_log['EX'].astype('float')
print("ex:",adfuller(ex))
lnex=quarter_log['LNEX'].astype('float')
print("lnex:",adfuller(lnex))
# lnex.plot()
# plt.show()
IM=quarter_log['IM'].astype('float')
print("IM:",adfuller(IM))
LNIM=quarter_log['LNIM'].astype('float')
print("LNIM:",adfuller(LNIM))
# LNIM.plot()
# plt.show()
# FDI=quarter_log['FDI'].astype('float')
# print("FDI:",adfuller(FDI))
# LNFDI=quarter_log['LNFDI'].astype('float')
# print("LNFDI:",adfuller(LNFDI))
RER=quarter_log['RER'].astype('float')
print("RER:",adfuller(RER))
LNRER=quarter_log['LNRER'].astype('float')
print("LNRER:",adfuller(LNRER))
# LNRER.plot()
# plt.show()
GDP=quarter_log['平减后的GDP'].astype('float')
print("GDP:",adfuller(GDP))
LNGDP=quarter_log['LNGDP'].astype('float')
print("LNGDP:",adfuller(LNGDP))
# LNGDP.plot()
# plt.show()


