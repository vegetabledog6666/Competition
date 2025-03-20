#!/usr/bin/env python
# coding: utf-8

# In[68]:


import numpy as np
import pandas as pd
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt
# 中文的使用
import matplotlib as mpl
mpl.rcParams["font.sans-serif"]=["kaiti"] # 设置中文字体
mpl.rcParams["axes.unicode_minus"]=False  # 设置减号不改变


# In[69]:


data = pd.read_excel(r"C:\Users\MATH_MGD\Desktop\22(7-9).xlsx").values

date = np.unique(data[:,0])

lines = np.unique([i[0]+i[1]for i in data[:,[1,2]]])
lines = np.array([[i[0],i[1]] for i in lines])

line_mean = []
line_min = []
xu = []
f_mean = []
f_std = []
mt = np.zeros(shape=(lines.shape[0],date.shape[0]))
for i in range(lines.shape[0]):
    d1 = data[np.logical_and(data[:,1]==lines[i,0],data[:,2]==lines[i,1])][:,-1]
    rq = data[np.logical_and(data[:,1]==lines[i,0],data[:,2]==lines[i,1])][:,0]
    line_mean+=[d1.mean()]
    line_min +=[d1.min()]
    gd =d1.mean()-2*d1.std()
    gd=0 if gd<0 else gd
    xu +=[gd]
    d2 = d1-(gd)
    f_mean += [d2.mean()]
    f_std += [d2.std()]
    for j in range(rq.shape[0]):
        mt[i,date==rq[j]] = d2[j]
xu = np.array(xu)
print("22年3季度固定需求",np.c_["1",lines,np.round(xu)])
print("22年3季度非固定需求均值标准差\n",np.c_["1",lines,np.round(f_mean,4),np.round(f_std,4)])


# In[70]:


pd.DataFrame(np.c_["1",lines,np.round(xu)],columns=["起点","终点","固定需求"]).to_excel(r"C:\Users\MATH_MGD\Desktop\第五问_固定需求(22年3季度).xlsx")


# In[71]:


pd.DataFrame(np.c_["1",lines,np.round(f_mean,4),np.round(f_std,4)],columns=["起点","终点","均值","标准差"]).to_excel(r"C:\Users\MATH_MGD\Desktop\第五问_非固定需求(均值与标准差)(22年3季度).xlsx")


# In[72]:


pd.DataFrame(np.c_["1",lines,mt],columns=np.r_["0",["起点","终点"],date]).to_excel(r"C:\Users\MATH_MGD\Desktop\第五问_非固定需求(22年3季度).xlsx")


# In[73]:


sc = np.array([["V","N"],["V","Q"],["J","I"],["O","G"]])


# In[74]:


i=0
for i in range(2):
    d1 = data[np.logical_and(data[:,1]==sc[i,0],data[:,2]==sc[i,1])][:,-1]
    d2 = d1-(d1.mean()-d1.min())
    # 示例数据（请用实际非固定需求数据替换）
    sample_data = d2.reshape(-1, 1)

    # KDE模型实例化
    kde = KernelDensity(kernel='gaussian', bandwidth=5).fit(sample_data)

    # 指定评估点（根据实际需求调整范围和间隔）
    evaluation_points = np.linspace(d2.min(), d2.max(), num=300).reshape(-1, 1)

    # 评估KDE模型
    log_density = kde.score_samples(evaluation_points)
    density = np.exp(log_density)

    # 绘制KDE结果和直方图
    fig, ax = plt.subplots()
    ax.plot(evaluation_points, density, label='KDE')
    ax.hist(sample_data, bins=5, density=True, alpha=0.5, color='blue', label='直方图')

    ax.set_xlabel(f'{sc[i,0]}->{sc[i,1]}(非固定需求)',fontsize=14)
    ax.set_ylabel('概率密度',fontsize=14)
    ax.legend(fontsize=14)
    plt.show()
    pd.DataFrame(np.c_["1",evaluation_points,density[:,None]],columns=["非固定需求量","概率密度"]).to_excel(r"C:\Users\MATH_MGD\Desktop\{}_{}(非固定需求).xlsx".format(sc[i,0],sc[i,1]))


# In[75]:


data = pd.read_excel(r"C:\Users\MATH_MGD\Desktop\23(1-3).xlsx").values

date = np.unique(data[:,0])

lines = np.unique([i[0]+i[1]for i in data[:,[1,2]]])
lines = np.array([[i[0],i[1]] for i in lines])

line_mean = []
line_min = []
xu = []
f_mean = []
f_std = []
mt = np.zeros(shape=(lines.shape[0],date.shape[0]))
for i in range(lines.shape[0]):
    d1 = data[np.logical_and(data[:,1]==lines[i,0],data[:,2]==lines[i,1])][:,-1]
    rq = data[np.logical_and(data[:,1]==lines[i,0],data[:,2]==lines[i,1])][:,0]
    line_mean+=[d1.mean()]
    line_min +=[d1.min()]
    gd =d1.mean()-2*d1.std()
    gd=0 if gd<0 else gd
    xu +=[gd]
    d2 = d1-(gd)
    f_mean += [d2.mean()]
    f_std += [d2.std()]
    for j in range(rq.shape[0]):
        mt[i,date==rq[j]] = d2[j]
xu = np.array(xu)
print("23年1季度固定需求",np.c_["1",lines,np.round(xu)])
print("23年1季度非固定需求均值标准差\n",np.c_["1",lines,np.round(f_mean,4),np.round(f_std,4)])


# In[76]:


pd.DataFrame(np.c_["1",lines,np.round(xu)],columns=["起点","终点","固定需求"]).to_excel(r"C:\Users\MATH_MGD\Desktop\第五问_固定需求(23年第1季度).xlsx")


# In[77]:


pd.DataFrame(np.c_["1",lines,np.round(f_mean,4),np.round(f_std,4)],columns=["起点","终点","均值","标准差"]).to_excel(r"C:\Users\MATH_MGD\Desktop\第五问_非固定需求(均值与标准差)(23年1季度).xlsx")


# In[78]:


pd.DataFrame(np.c_["1",lines,mt],columns=np.r_["0",["起点","终点"],date]).to_excel(r"C:\Users\MATH_MGD\Desktop\第五问_非固定需求(23年1季度).xlsx")


# In[79]:


for i in range(2,4):
    d1 = data[np.logical_and(data[:,1]==sc[i,0],data[:,2]==sc[i,1])][:,-1]
    d2 = d1-(d1.mean()-d1.min())
    # 示例数据（请用实际非固定需求数据替换）
    sample_data = d2.reshape(-1, 1)

    # KDE模型实例化
    kde = KernelDensity(kernel='gaussian', bandwidth=5).fit(sample_data)

    # 指定评估点（根据实际需求调整范围和间隔）
    evaluation_points = np.linspace(d2.min(), d2.max(), num=300).reshape(-1, 1)

    # 评估KDE模型
    log_density = kde.score_samples(evaluation_points)
    density = np.exp(log_density)

    # 绘制KDE结果和直方图
    fig, ax = plt.subplots()
    ax.plot(evaluation_points, density, label='KDE')
    ax.hist(sample_data, bins=5, density=True, alpha=0.5, color='blue', label='直方图')

    ax.set_xlabel(f'{sc[i,0]}->{sc[i,1]}(非固定需求)',fontsize=14)
    ax.set_ylabel('概率密度',fontsize=14)
    ax.legend(fontsize=14)
    plt.show()
    pd.DataFrame(np.c_["1",evaluation_points,density[:,None]],columns=["非固定需求量","概率密度"]).to_excel(r"C:\Users\MATH_MGD\Desktop\{}_{}(非固定需求).xlsx".format(sc[i,0],sc[i,1]))


# In[ ]:





# In[ ]:





# In[ ]:




