import numpy as np
import pandas as pd
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams["font.sans-serif"]=["SimHei"]
mpl.rcParams["axes.unicode_minus"]=False 

data = pd.read_excel("C:\\Users\\Administrator\\Desktop\\vs工作界面\\22年季度数据.xlsx").values

date = np.unique(data[:,0])     ##表示全部数据

lines = np.unique([i[0]+i[1]for i in data[:,[1,2]]])
lines = np.array([[i[0],i[1]] for i in lines])    ##表示总共的城市对

line_mean = []
line_min = []
xu = []
f_mean = []
f_std = []
mt = np.zeros(shape=(lines.shape[0],date.shape[0]))
print(mt)
for i in range(lines.shape[0]):
    d1 = data[np.logical_and(data[:,1]==lines[i,0],data[:,2]==lines[i,1])][:,-1]  ##d1为相对应的月份的数据
    rq = data[np.logical_and(data[:,1]==lines[i,0],data[:,2]==lines[i,1])][:,0]   ##rq为相对应的时间序列的数据
    line_mean+=[d1.mean()]     ##表示每个城市对的均值
    line_min +=[d1.min()]      ##表示每个城市对的最小值
    fixed =d1.mean()-2*d1.std()   ##表示3sigma定则
    if(fixed<0):
        fixed=0
    xu +=[fixed]
    notfixed = d1-(fixed)       ##代表各个城市对的非固定需求
    
    ##以下则为计算均值与标准差
    f_mean += [notfixed.mean()]
    f_std += [notfixed.std()]
    for j in range(rq.shape[0]):
        mt[i,date==rq[j]] = notfixed[j]
xu = np.array(xu)
print("22年固定需求",np.c_["1",lines,np.round(xu)])
print("22年非固定需求均值标准差\n",np.c_["1",lines,np.round(f_mean,4),np.round(f_std,4)])

temp=pd.DataFrame(np.c_["1",lines,np.round(xu)],columns=["发货城市","收货城市","固定需求"])
temp.to_excel("C:\\Users\\Administrator\\Desktop\\vs工作界面\\固定需求(22年).xlsx")

temp=pd.DataFrame(np.c_["1",lines,np.round(f_mean,2),np.round(f_std,2)],columns=["发货城市","收货城市","均值","标准差"])
temp.to_excel("C:\\Users\\Administrator\\Desktop\\vs工作界面\\非固定需求(均值与标准差)(22年).xlsx")

temp=pd.DataFrame(np.c_["1",lines,mt],columns=np.r_["0",["发货城市","收货城市"],date])
temp.to_excel("C:\\Users\\Administrator\\Desktop\\vs工作界面\\非固定需求(22年).xlsx")



sc = np.array([["V","N"],["V","Q"]])
i=0
for i in range(2):
    d1 = data[np.logical_and(data[:,1]==sc[i,0],data[:,2]==sc[i,1])][:,-1]
    fixed =d1.mean()-2*d1.std()      ##求出固定需求常数，即3sigma准则
    if(fixed<0):
        fixed=0
    d2 = d1-fixed
    sample_data = d2.reshape(-1, 1)

    # KDE模型实例化,高斯核函数是一个常用的核函数，可以对连续变量进行估计，带宽参数影响核函数的宽度，决定了估计出的概率密度函数的平滑度。
    kde = KernelDensity(kernel='gaussian', bandwidth=6).fit(sample_data)

    # 指定评估点（根据实际需求调整范围和间隔）
    ep = np.linspace(d2.min(), d2.max(), num=300).reshape(-1, 1)

    # 评估KDE模型
    ld = kde.score_samples(ep)
    ds = np.exp(ld)

    # 绘制KDE结果和直方图
    fig, ax = plt.subplots()
    ax.plot(ep, ds, label='KDE')
    ax.hist(sample_data, bins=5, density=True, alpha=0.5, color='blue', label='直方图')

    ax.set_xlabel('{}到{}(非固定需求)'.format(sc[i,0],sc[i,1]),fontsize=15)
    ax.set_ylabel('概率密度',fontsize=14)
    ax.legend(fontsize=14)
    plt.savefig('{}到{}(非固定需求)分布图.png'.format(sc[i,0],sc[i,1]))
    plt.show()
    temp=pd.DataFrame(np.c_["1",ep,ds[:,None]],columns=["非固定需求量","概率密度"])
    temp.to_excel("C:\\Users\\Administrator\\Desktop\\vs工作界面\\{}_{}(非固定需求).xlsx".format(sc[i,0],sc[i,1]))