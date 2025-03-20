library(ggplot2)
library(readxl)
data=read_excel("V:\\大数据分析相关文件\\R\\人口增长倒数后10表.xlsx")
colnames(data)<-c("id","coun","val")

coun=list(data['coun'])
coun=unlist(coun)

num=list(data['val'])
num=unlist(num)
num=as.numeric(num)
ggplot(mapping=aes(x=reorder(coun,num),y=num))+
  geom_bar(stat="identity",fill="green")+
  labs(x="国家（增长皆为负数）",y="增长绝对数")+
  theme(
    axis.title.x=element_text(size=12),
    axis.text.x=element_text(size=9)
  )+geom_text(aes(label=num),vjust=-0.5)