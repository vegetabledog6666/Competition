import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']

year=np.arange(1950,2101)
pop_predic=11.499322e+09/(1+(11/2.5-1)*np.e**(-0.02731*(year-1950)))     ##相应的预测曲线
pop_ori=pd.read_excel(r"C:\Users\Administrator\Desktop\vs工作界面\世界总人口变化.xls",usecols=["Population"])  ##读入原始数据
pop_ori=np.array(pop_ori)


plt.plot(np.arange(1950,2023),pop_ori,lw=0.4,color="b",linestyle="-",label="世界人口真实曲线")
plt.plot(year,pop_predic,lw=0.8,color="r",linestyle=":",label="世界人口拟合曲线")
plt.title("1950到2100年世界人口预测图")
plt.legend()
plt.show()

data=pd.DataFrame(data=[year,pop_ori,pop_predic],index=["年份","原始数据人口","预测人口"])
data.to_excel("世界人口预测.xls")
