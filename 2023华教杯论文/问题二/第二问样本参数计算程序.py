import numpy as np
import pandas as pd
import sympy
from scipy.integrate import simpson
s_xyz=pd.read_excel("相乘固定值.xlsx",index_col=0)
ori_R=pd.read_excel("不同样本不同波长下R值.xlsx",index_col=0)
tar_x=pd.DataFrame()
bo_chang=[]
for i in range(400,701,20):
    bo_chang.append(i)

for i in range(0,ori_R.shape[1]):
    new_col=list(np.array(ori_R[i+1])*np.array(s_xyz["S(λ)x ̅(λ)"])*20)
    new_col=0.1*simpson(new_col,bo_chang)
    tar_x=pd.concat([tar_x,pd.DataFrame({i+1:[new_col]})],axis=1)

tar_y=pd.DataFrame()
for i in range(0,ori_R.shape[1]):
    new_col=list(np.array(ori_R[i+1])*np.array(s_xyz["S(λ)y ̅(λ)"])*20)
    new_col=0.1*simpson(new_col,bo_chang)
    tar_y=pd.concat([tar_y,pd.DataFrame({i+1:[new_col]})],axis=1)

tar_z=pd.DataFrame()
for i in range(0,ori_R.shape[1]):
    new_col=list(np.array(ori_R[i+1])*np.array(s_xyz["S(λ)z ̅(λ)"])*20)
    new_col=0.1*simpson(new_col,bo_chang)
    tar_z=pd.concat([tar_z,pd.DataFrame({i+1:[new_col]})],axis=1)
    
k=0
##以上为算刺激值
##以下为色差计算的值
tar_x.rename(index={0:"x"},inplace=True)
tar_y.rename(index={0:"y"},inplace=True)
tar_z.rename(index={0:"z"},inplace=True)
tar_l=pd.DataFrame(index=["l"],columns=tar_x.columns.values)
tar_a=pd.DataFrame(index=["a"],columns=tar_x.columns.values)
tar_b=pd.DataFrame(index=["b"],columns=tar_x.columns.values)



for j in tar_x.columns.values:   ###用于计算目标的lab，求色差
    if(((tar_y.loc["y",j]/100)>0.008856)&((tar_x.loc["x",j]/94.83)>0.008856)&((tar_z.loc["z",j]/107.38)>0.008856)):
        tar_l.loc["l",j]=116*(tar_y.loc["y",j]/100)**(1/3)-16
        tar_a.loc["a",j]=500*((tar_x.loc["x",j]/94.83)**(1/3)-(tar_y.loc["y",j]/100)**(1/3))
        tar_b.loc["b",j]=200*((tar_y.loc["y",j]/100)**(1/3)-(tar_z.loc["z",j]/107.38)**(1/3))
    else:
        tar_l.loc["l",j]=903.3*(tar_y.loc["y",j]/100)
        tar_a.loc["a",j]=3893.5*((tar_x.loc["x",j]/94.83)-(tar_y.loc["y",j]/100))
        tar_b.loc["b",j]=1557.4*((tar_y.loc["y",j]/100)-(tar_z.loc["z",j]/107.38))
        
middle_result=pd.concat([tar_x,tar_y,tar_z,tar_l,tar_a,tar_b])
middle_result.to_excel("各个样本的参数.xls")