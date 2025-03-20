def deal(excel):
  
  chn=list()
  fra=list()
  ind=list()
  isr=list()
  prk=list()
  pak=list()
  rus=list()
  zaf=list()
  gbr=list()
  usa=list()
  x=range(2002,2023,1)

  for rown in range(excel.nrows):
   c=table.cell_value(rown,1)
   y=table.cell_value(rown,2)
   if(c=="Abbreviation"):
       continue
   if(y!=2002)and(y!=2022):
     continue
   cha=table.cell_value(rown,3)
   if(c=="CHN"):
     chn.append(cha)
   elif(c=="FRA"):
     fra.append(cha)
   elif(c=="IND"):
     ind.append(cha)
   elif(c=="ISR"):
     isr.append(cha)
   elif(c=="PRK"):
     prk.append(cha)
   elif(c=="PAK"):
     pak.append(cha)
   elif(c=="RUS"):
     rus.append(cha)
   elif(c=="ZAF"):
     zaf.append(cha)
   elif(c=="GBR"):
     gbr.append(cha)
   else :
     usa.append(cha)
  
  chn.append(chn[1]-chn[0])
  fra.append(fra[1]-fra[0])
  ind.append(ind[1]-ind[0])
  isr.append(isr[1]-isr[0])
  prk.append(prk[1]-prk[0])
  pak.append(pak[1]-pak[0])
  rus.append(rus[1]-rus[0])
  zaf.append(zaf[1]-zaf[0])
  gbr.append(gbr[1]-gbr[0])
  usa.append(usa[1]-usa[0])

  al=list()
  al.append(chn+["中国"])
  al.append(fra+["法国"])
  al.append(ind+["印度"])
  al.append(isr+["以色列"])
  al.append(prk+["朝鲜"])
  al.append(pak+["巴基斯坦"])
  al.append(rus+["俄罗斯"])
  al.append(zaf+["南非"])
  al.append(gbr+["英国"])
  al.append(usa+["美国"])

  ##以下是导出数据
  wb=xlwt.Workbook()
  ws=wb.add_sheet("Text")

  ws.write(0,0,"国家")
  ws.write(0,1,"2002年拥有核武器")
  ws.write(0,2,"2022年拥有核武器")
  ws.write(0,3,"核武器数量变化值")
  for i in range(0,len(al)):##导出到Excel表中
    ws.write(i+1,0,al[i][3])
    ws.write(i+1,1,al[i][0])
    ws.write(i+1,2,al[i][1])
    ws.write(i+1,3,al[i][2])
  wb.save("./核武差值表.xls")
  
import xlwt
import matplotlib.pyplot as plt
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] =False
import xlrd

data=xlrd.open_workbook(r'过去20年核弹数量变化.xlsx')
table=data.sheets()[0]
deal(table)
