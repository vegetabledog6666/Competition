def deal(excel):
  
  ynot=dict()
  ypos=dict()
  x=list()

  for rown in range(excel.nrows):
   y=table.cell_value(rown,2)    ##记录年份
   if(y=="Year"):
       continue       ##省去第一行
   y=int(y)
   
   country=table.cell_value(rown,0)##表示国家
   status=table.cell_value(rown,3)##表示状态
   if((country not in ynot.keys())and(status==0)):
     ynot[country]=y
   if((country not in ypos.keys())and(status==3)):
     ypos[country]=y

  
  country=ypos.keys()    ##只计算有核弹的国家，有些国家就没想有过
  time=dict()
  for i in country:     ##两两相互减去
    time[i]=ypos[i]-ynot[i]
  time=list(sorted(time.items(),key=lambda d:d[1]))   ##排下序
  print("{} has made the fastest transition from 'not considering nuclear weapons' to 'possessing nuclear weapons',it costs {} years".format(time[0][0],time[0][1]))

  ##以下是导出数据
  wb=xlwt.Workbook()
  ws=wb.add_sheet("Text")

  ws.write(0,0,"国家")
  ws.write(0,1,"耗费时间")
  ws.write(0,2,"获得核武器年份")
  for i in range(0,len(time)):##导出到Excel表中
    ws.write(i+1,0,time[i][0])
    ws.write(i+1,1,time[i][1])
    ws.write(i+1,2,ypos[time[i][0]])
  wb.save("./不同国家拥有核武器时间表.xls")

import xlwt
import matplotlib.pyplot as plt
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] =False
import xlrd

data = xlrd.open_workbook(r'position.xlsx')
table = data.sheets()[0]
deal(table)
