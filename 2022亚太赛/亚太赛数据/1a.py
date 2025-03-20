def deal(excel):
  coun=dict()
  for rown in range(excel.nrows):
   c=table.cell_value(rown,0)    ##记录国家
   if(c=="Country"):    ##去掉第一行，如果是第一行的话就是标签
       continue
   if(table.cell_value(rown,3)>0):##如果大于1说明有核武
       coun[c]=1
    
  for i in coun.keys():
      if(coun[i]==1):##直接输出就好
        print(i)

    
import xlrd
data = xlrd.open_workbook(r'stockpiles.xlsx')
table = data.sheets()[0]
deal(table)
