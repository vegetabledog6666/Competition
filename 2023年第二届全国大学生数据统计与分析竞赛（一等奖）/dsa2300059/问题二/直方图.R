mydata<-read.csv("Brazil.csv")
mydata1<-read.csv("Russia1.csv")
mydata2<-read.csv("Japan1.csv")
a<-ggplot(mydata,aes(x=Age.interval,y=Population.rate))+
  geom_bar(stat="identity",color="#199999",fill="#199999")+
  xlab("Age range of Brazil")+
  ylab("")
b<-ggplot(mydata1,aes(x=Age.interval,y=Population.rate))+
  geom_bar(stat="identity",color="#A6B4E1",fill="#A6B4E1")+
  xlab("Age range of Russia")+
  ylab("Frequency/Class interval")
c<-ggplot(mydata2,aes(x=Age.interval,y=Population.rate))+
  geom_bar(stat="identity",color="#36B4E9",fill="#36B4E9")+
  xlab("Age range of Japan")+
  ylab("")
Rmisc::multiplot(a,b,c,line=3)