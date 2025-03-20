import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']

pop_ori=pd.read_excel(r"C:\Users\Administrator\Desktop\vs工作界面\中国总人口变化.xls",usecols=["Population"])
pop_ori.dropna(how="any",inplace=True)
pop_ori=np.array(pop_ori)

pop_predic=pd.read_excel(r"C:\Users\Administrator\Desktop\vs工作界面\中国人口预测.xlsx",usecols=["total_pop"])
pop_predic=np.array(pop_predic)
pop_predic=pop_predic*10000

plt.plot(np.arange(1950,2023),pop_ori,lw=2,color="b",linestyle="-",label="中国人口真实曲线")
plt.plot(np.arange(2023,2101),pop_predic,lw=4,color="r",linestyle=":",label="中国人口预测曲线")
plt.title("2023到2100年中国人口预测图")
plt.legend()
plt.show()
