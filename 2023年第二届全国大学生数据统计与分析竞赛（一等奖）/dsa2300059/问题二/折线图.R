data<-read.csv("rate1.csv")
data1<-read.csv("rate.csv")
a<-ggplot(data,aes(x=Year,y=Aging.rate,color=Country))+
  geom_line(size=0.8)+ylab("Under 15")+
  theme(legend.position = "bottom")
b<-ggplot(data1,aes(x=Year,y=Aging.rate,color=Country))+
  geom_line(size=0.8)+ylab("Over 64")+
  theme(legend.position = "bottom")
Rmisc::multiplot(b,a,cols=2)