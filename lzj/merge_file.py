# -*- coding: utf-8 -*-
'''
Created on 2018年12月24日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import pandas as pd
def merge_file(dir,j,file1,file2):
    file_1_2=pd.DataFrame()
    file_1=pd.read_csv(file1,engine='python')
    file_2=pd.read_csv(file2,engine='python')
    file_1_1=file_1.dropna()
    file_2_1=file_2.dropna()
    word_cx=[]
    word_time=[]
    for index1,i in file_1_1.iterrows():
        for index2,k in file_2_1.iterrows():
#             print(k['出现次数'])
            if i['词性']==k['词性']:
                word_cx.append(i['词性'])
                word_time.append(int(i['出现次数'])+int(k['出现次数']))
    for index, m in file_1_1.iterrows():
        if m['词性'] not in word_cx:
                word_cx.append(m['词性'])
                word_time.append(int(m['出现次数']))
    for index,n in file_2_1.iterrows():
        if n['词性'] not in word_cx:
                word_cx.append(n['词性'])
                word_time.append(int(n['出现次数']))
    print(word_cx)
    print(word_time)
    file_1_2['词性']=word_cx  
    file_1_2['出现次数']=word_time
    file_1_2=file_1_2.sort_values(by="出现次数" , ascending=False)
    path=r'./cixing/'+dir+'/小说词性'+str(j)+'元文法统计.csv'
    file_1_2[0:19].to_csv(path)
        
#     print(file_1_1,file_2_1)
if __name__ == '__main__':
    sec_dir=['军事','历史','灵异','奇幻','体育','武侠','现实','玄幻','游戏']
    for dir in sec_dir:
        for j in range(2,6):
            path1 = './词性/'+dir+'/成功小说词性'+str(j)+'元文法统计.csv'
            path2 = './词性/'+dir+'/不成功小说词性'+str(j)+'元文法统计.csv'
            merge_file(dir,j,path1, path2)
        