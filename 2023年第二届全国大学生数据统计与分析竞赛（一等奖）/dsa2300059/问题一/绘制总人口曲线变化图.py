import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']

data=pd.read_excel(r"C:\Users\Administrator\Desktop\vs工作界面\世界总人口变化.xls",usecols=["Year","Population"])
fig=plt.figure(figsize=(4, 4), dpi=150)
plt.plot(data["Year"],data["Population"],lw=3,ls='-',c='b',alpha=0.5,label="人口变化曲线")
plt.title(label="1950到2021世界人口变化图")
for i in range(0,71,10):
    plt.text(data["Year"][i]-2,data["Population"][i]*0.90,s="{}:{}亿".format(data["Year"][i],round(data["Population"][i]/(100000000),2)),fontsize=6)
plt.legend()
plt.show()