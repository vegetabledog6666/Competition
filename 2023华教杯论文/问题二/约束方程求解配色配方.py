import numpy as np
import sympy
from scipy.optimize import minimize
from scipy.integrate import simpson
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
inf_samp=pd.read_excel("各个样本的参数.xls",index_col=0)
Ks_samp=pd.read_excel("不同样本不同波长下KS值.xls")
ori=pd.read_excel("配色剂读入数据.xlsx")
ori_use=ori.iloc[0,:]

nummer=0
use=pd.read_excel("各颜色各波长单位K比S表.xlsx")
data=pd.read_excel("各颜色各波长单位K比S表.xlsx")
Sx=pd.read_excel("相乘固定值.xlsx")
red=np.array(data["red"])
yellow=np.array(data["yellow"])
blue=np.array(data["blue"])


def get_answer(r,y,b,samp):
    global inf_samp,red,yellow,blue,Sx,ans
    ll_tar=inf_samp.loc["l",samp]
    aa_tar=inf_samp.loc["a",samp]
    bb_tar=inf_samp.loc["b",samp]
    
    cur_Ks=red*r+yellow*y+blue*b
    cur_R=[]
    for i in range(0,len(cur_Ks)):
        x=sympy.Symbol("x")
        equation = sympy.Eq((1-x**2)/(2*x), cur_Ks[i])
        result=sympy.solve(equation,x)
        cur_R.append(result[1])
    
    x=[]
    for i in range(400,701,20):
        x.append(i)
    
    cur_R=np.array(cur_R)
    X=0.1*simpson(cur_R*np.array(Sx["S(λ)x ̅(λ)"])*20,x)
    Y=0.1*simpson(cur_R*np.array(Sx["S(λ)y ̅(λ)"])*20,x)
    Z=0.1*simpson(cur_R*np.array(Sx["S(λ)z ̅(λ)"])*20,x)

    if(((Y/100)>0.008856)&((X/94.83)>0.008856)&((Z/107.38)>0.008856)):
        cur_l=116*(Y/100)**(1/3)-16
        cur_a=500*((X/94.83)**(1/3)-(Y/100)**(1/3))
        cur_b=200*((Y/100)**(1/3)-(Z/107.38)**(1/3))
    else:
        cur_l=903.3*(Y/100)
        cur_a=3893.5*((X/94.83)-(Y/100))
        cur_b=1557.4*((Y/100)-(Z/107.38))
    
    delta_l=ll_tar-cur_l
    Cs=(aa_tar**2+bb_tar**2)**0.5-(cur_a**2+cur_b**2)**0.5
    Cc=((aa_tar-cur_a)**2+(bb_tar-cur_b)**2)**0.5
    delta_h=(Cc**2-Cs**2)**0.5
    
    delta_e=(delta_l**2+Cs**2+delta_h**2)**0.05
    
    ans=ans.append({"red":r,"yellow":y,"blue":b,"color_difference":delta_e},ignore_index=True)
    return delta_e

def func(args):
    global sample,inf_samp
    fun=lambda x:get_answer(x[0],x[1],x[2],sample)
    return fun

def con(args):      ###让k/s进行匹配
    global Ks_target
    cons=()
    
    for i in range(0,16):
        r=red[i]
        y=yellow[i]
        b=blue[i]
        target=Ks_target[i]
        cons+=({"type":"ineq","fun":lambda x:r*x[0]+y*x[1]+b*x[2]+0.3-target},)  ##x*yueshu>target-0.3，0.3是   K/S值设定的下节
        cons+=({"type":"ineq","fun":lambda x:target+0.3-(r*x[0]+y*x[1]+b*x[2])},)  ##x*yueshu<target+0.3，0.3是K/S值设定的上节
        
    cons+=({"type":"ineq","fun":lambda x:x[0]},)
    cons+=({"type":"ineq","fun":lambda x:x[1]},)
    cons+=({"type":"ineq","fun":lambda x:x[2]},)
    return cons 

args=()
args1=()
for sample in range(1,11): ##单单抽出每个样本来求
    Ks_target=np.array(Ks_samp[sample])
    x0=np.array([0 for j in range(3)])
    cons=con(args1)
    ans=pd.DataFrame(columns=["red","yellow","blue","color_difference"])
    res=minimize(func(args),x0,method='SLSQP',constraints=cons)
    ans.to_excel("样本{}相对应计算结果.xlsx".format(sample))
    print(sample)
