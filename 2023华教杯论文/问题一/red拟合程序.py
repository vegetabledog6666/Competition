import pandas as pd
import xlwt
import numpy as np
from scipy.optimize import curve_fit

def func1(x,a,b):
    return a+b*x

data=pd.read_excel("C:\\Users\\Administrator\\Desktop\\vs工作界面\\问题一红色拟合.xlsx")
C=list(data["浓度（%）"].T)
xdata = np.array(C) # 自变量
cols=["波长","拟合函数","拟合系数","b"]
book = xlwt.Workbook(encoding='utf-8')
sheet = book.add_sheet('sheet',cell_overwrite_ok=True)
for i in range(0,len(cols)):
    sheet.write(0,i,cols[i])
k=1


for i in range(400,701,20):
    st=str(i)+"nm"
    cur=list(data[st])
    ydata = np.array(cur) # 因变量
    popt, pcov = curve_fit(func1, xdata, ydata)
    
    calc_ydata = [func1(i, popt[0], popt[1]) for i in xdata]
    res_ydata = np.array(ydata) - np.array(calc_ydata)
    ss_res = np.sum(res_ydata ** 2)
    ss_tot = np.sum((ydata - np.mean(ydata)) ** 2)
    r_squared1 = 1 - (ss_res / ss_tot)
    
    popt=np.round(popt,4)
    sheet.write(k,0,st)
    sheet.write(k,1,"y={}+{}*x".format(popt[0],popt[1]))
    sheet.write(k,2,r_squared1)
    sheet.write(k,3,popt[1])
    k+=1
book.save("红色拟合结果.xls")
