import pylab
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
data=pd.read_excel("长三角地区新能源汽车保有量.xlsx",usecols=["长三角"])
y=list(data["长三角"])
x=list(range(2014,2023))

z1=np.polyfit(x, y, 3)
p1=np.poly1d(z1)
print(p1)

xnew=list(range(2014,2026))
y_pred=p1(xnew)

y.extend(y_pred[-3:])

plot1=pylab.plot(xnew, y, '*', label='original values')
plot2=pylab.plot(xnew, y_pred, 'r', label='fit values')

for xx,yy in zip(xnew,y):
    plt.text(xx+0.1,np.round(yy,3),"x={}\ny={}".format(xx,np.round(yy,3)))
pylab.title('2014到2022年长三角地区新能源汽车保有量拟合图（后3年为预测结果）')
pylab.xlabel('年份')
pylab.ylabel('万辆')
pylab.legend(loc=2)
pylab.show()