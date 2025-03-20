def deal(excel):
  
  year=dict()
  x=list()

  for rown in range(excel.nrows):
   y=table.cell_value(rown,2)    ##记录年份
   if(y=="Year"):
       continue       ##省去第一行
   y=int(y)
   if(y not in year.keys()):     ##如果没有出现过该年份先给它赋值
     year[y]=table.cell_value(rown,3) 
   else :##出现了直接加上就好
     year[y]+=table.cell_value(rown,3)

  num=year.values()##y值，即总的核弹实验数据
  x=year.keys()##x坐标值，即年份
  plt.plot(x, num, "b-.",label=u'The Number of nuclear bomb tests')
  plt.legend()

  plt.xlabel(u"YEAR")
  plt.ylabel("The Number of nuclear bomb tests")
  plt.title("The Number of nuclear bomb tests from 1945 to 2019")
  plt.show()

  maxn=0;low=0;high=0
  for i in range(1949,2016):##五年五年的进行遍历
    temp=0   ##计算其临时值
    for j in range(i,i+5):
      temp+=year[j]
    if(temp>maxn):##找到最大的就更新一下
      maxn=temp
      low=i
      high=i+4
  print("从{}到{}间核弹实验次数最多，为{}".format(low,high,maxn))

import matplotlib.pyplot as plt
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] =False
import xlrd

data = xlrd.open_workbook(r'tests.xlsx')
table = data.sheets()[0]
deal(table)
