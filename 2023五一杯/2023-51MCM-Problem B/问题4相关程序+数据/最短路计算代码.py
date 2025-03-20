import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from copy import deepcopy
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False


fixeddata=pd.read_excel("C:\\Users\\Administrator\\Desktop\\vs工作界面\\附件3.xlsx")

##以下为提取相对应的数据
sta=fixeddata.loc[:,"起点 (Start)"]
end=fixeddata.loc[:,"终点 (End)"]
fixcos=fixeddata.loc[:,"固定成本 (Fixed cost)"]
dot_inf=dict()
ori=nx.DiGraph()


##以下表示给相对应的路径编码，并插入到图中
wegnum=0
weg=dict()
for i in range(len(sta)):
    weg[wegnum]=(sta[i],end[i])
    wegnum+=1
    dot_inf[(sta[i],end[i])]=fixcos[i]
    ori.add_edge(sta[i],end[i],weight=fixcos[i])

pos=nx.shell_layout(ori)##表示画图的格式，下面是画图相关代码
nx.draw_networkx(ori,pos=pos,node_size=200,node_shape='o',width=1,style='solid',font_size=8)

node_labels=nx.get_node_attributes(ori,"des")
nx.draw_networkx_labels(ori,pos=pos,labels=node_labels)
plt.title("铁路路线图",fontsize=10)
plt.show()

nodes=[]
for i in ori.nodes.data():
    nodes.append(i[0])

node=dict()
letters=dict()
for i in range(0,len(nodes)):##表示对于点进行编码
    node[nodes[i]]=i
    letters[i]=nodes[i]

dist=dict()
pre=dict()
INF=9999999
def bellman_ford(bgi,end,weight):##最短路算法
    backup=dict()
    for i in range(0,len(node)):
        dist[i]=INF
    
    dist[bgi]=0
    for i in range(0,5):##限制次数为5
        backup=deepcopy(dist)
        for j in range(0,wegnum): ##代表走wegnum条路
            wega=node[weg[j][0]]
            wegb=node[weg[j][1]]
            w=dot_inf[weg[j]]*(1+(weight/200)**3)##计算对应的成本
            if(dist[wegb]>backup[wega]+w):
                dist[wegb]=backup[wega]+w
    return dist[end]
    
for j in range(23,28):##代表逐天读取，并且进行逐天预测
    g=nx.DiGraph()
    data=pd.read_excel("C:\\Users\\Administrator\\Desktop\\vs工作界面\\{}日数据.xlsx".format(str(j)))
    dci=data["发货城市 (Delivering city)"]
    rci=data["收货城市 (Receiving city)"]
    num=data["快递运输数量(件) (Express delivery quantity (PCS))"]


    today=0
    for i in range(0,len(dci)):
            start=node[dci[i]]
            end=node[rci[i]]
            today+=bellman_ford(start,end,num[i])
    print("4月{}日的最低运输成本是{}".format(j,today))