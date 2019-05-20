'''
Created on 2019年5月20日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense,LSTM,Dropout
import matplotlib.pyplot as plt
import glob,os
import seaborn as sns
import sys
from sklearn.preprocessing import MinMaxScaler

columns= ['YEARS','MONTH','DAY','TEMP_HIG','TEMP_COL','AVG_TEMP','AVG_WET','DATA_COL']
data=pd.read_csv('./1.csv',names=columns)
#print(data.head())

plt.figure(figsize=(24,8))
for i in range(8):
    plt.subplot(8,1,i+1)
    plt.plot(data.values[:,i])
    plt.title(columns[i],y=.5,loc='right')
#plt.show()

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg

scaler=MinMaxScaler(feature_range=(0,1))
scaler_data=scaler.fit_transform(data[['DATA_COL','TEMP_HIG','TEMP_COL','AVG_TEMP','AVG_WET']].values)
#print(scaler_data)
#print('**************')
reframed=series_to_supervised(scaler_data,1,1)
#print(reframed.info())
reframed.drop(reframed.columns[[6,7,8,9]],axis=1,inplace=True)

#print(reframed.info())
#print(reframed.head())

train_days=400
valid_days=150
values=reframed.values
train=values[:train_days,:]
valid=values[train_days:train_days+valid_days,:]
test=values[train_days+valid_days:,:]
train_X,train_y=train[:,:-1],train[:,-1]
valid_X,valid_y=valid[:,:-1],valid[:,-1]
test_X,test_y=test[:,:-1],test[:,-1]
print(train_X.shape, train_y.shape, valid_X.shape, valid_y.shape, test_X.shape, test_y.shape)
train_X=train_X.reshape((train_X.shape[0],1,train_X.shape[1]))
valid_X = valid_X.reshape((valid_X.shape[0], 1, valid_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
print(train_X.shape[1],train_X.shape[2])
print(train_X.shape, train_y.shape, valid_X.shape, valid_y.shape, test_X.shape, test_y.shape)
model1 = Sequential()
model1.add(LSTM(50, activation='relu',input_shape=(train_X.shape[1],train_X.shape[2]), return_sequences=False))
model1.add(Dense(1, activation='linear'))
model1.compile(loss='mean_squared_error', optimizer='adam')
# fit network
LSTM1 = model1.fit(train_X, train_y, epochs=100, batch_size=32, validation_data=(valid_X, valid_y), verbose=2, shuffle=False)
# plot history
plt.plot(LSTM1.LSTM['loss'], label='train')
plt.plot(LSTM1.LSTM['val_loss'], label='valid')
plt.legend()
plt.show()
