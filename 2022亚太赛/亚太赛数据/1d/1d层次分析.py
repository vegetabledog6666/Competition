import numpy as np
import xlrd
from sklearn import preprocessing
min_max=preprocessing.MinMaxScaler()


#计算特征向量和最大特征值
a=np.array([[1,1/5],[5,1]])  #a为自己构造的输入判别矩阵
w=np.linalg.eig(a)  #np.linalg.eig(matri)返回特征值和特征向量
tzz=np.max(w[0])  #最大特征值
t=np.argwhere(w[0]==tzz)#寻找最大特征值所在的行和列
tzx=w[1][::-1,t[0]]   #最大特征值对应的特征向量

#一致性检验
RILIST=[0,0,0.58,0.9,1.12,1.24,1.32,1.41,1.45,1.49,1.52,1.54,1.56,1.58,1.59]
n=a.shape[0]
RI=RILIST[n]
CI=(tzz-n)/(n-1)
CR=CI/RI
print(CR)
if CR<0.1:
    print("consistency test passed")
else :
    print("consistency test not passed")

data = xlrd.open_workbook(r'用于分析表.xlsx')
table=data.sheets()[0]

temp=list()
for rown in range(table.nrows):
    inc=table.cell_value(rown,1)
    rea=table.cell_value(rown,2)
    if(inc=="核弹增量"):
        continue
    temp.append([inc,rea])
    

P=np.array(temp) #每一行代表一个对象的指标评分
P=min_max.fit_transform(P)
#赋权重
quan=np.zeros((n,1));
quan=tzx/sum(tzx)
Q=quan

#显示出所有评分对象的评分值
score=np.dot(P,Q)   #矩阵乘法
for i in range(len(score)):
    print('The scores of number{:}={:}'.format(i+1,score[i,0].real))
