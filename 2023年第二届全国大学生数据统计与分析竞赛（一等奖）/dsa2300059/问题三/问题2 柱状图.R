library(dplyr)
library(ggplot2)
library(RColorBrewer)

u = getwd()
setwd(u)

df<-read.csv("各国人口（降序）.csv",header=TRUE,stringsAsFactors = FALSE)
df1 <- arrange(df, Population)
df1$rank <- c(1:223)
df1$x <- ifelse(df1$rank <= 10, "后十名国家", ifelse(df1$rank >= 214, "前十名国家", "中间国家"))
df1$Country_name<-factor(df1$Country_name,levels = unique(df1$Country_name),ordered = T)
m = max(df1$Population)


#所有国家柱形图制作
p1 <- ggplot(data=df1,aes(x = Country_name,y = Population,fill = x))+
        geom_bar(stat = "identity")+
        ggtitle("Histogram of the total population of countries in 2021")+
        geom_text(aes(label=Population),size=4.8,hjust=-0.1)+
        xlab("Country")+ 
        ylim(0,m*1.2)+
        ylab("Population")+
        coord_flip()+
        labs(fill="")+
        scale_fill_manual(values = c('前十名国家' = "red", '中间国家' = "grey80", '后十名国家' ="blue"))+
        #scale_fill_discrete(labels=c("前十名国家", "中间国家", "后十名国家"))+  
        theme(axis.title = element_text(size=30,face="plain",color="black"),
              axis.text = element_text(color = "black"),
              panel.background=element_rect(fill="white",colour=NA),
              panel.grid.major = element_line(colour = "grey20",size=0.25,linetype ="dotted" ),
              panel.grid.minor = element_line(colour = "grey20",size=0.25,linetype ="dotted" ))
p1


#后20名国家柱形图制作
df2 <- df1[df1$rank <= 20,]
m2 = max(df2$Population)
p2 <- ggplot(data=df2,aes(x = Country_name,y = Population,fill = x))+
  geom_bar(stat = "identity")+
  ggtitle("Bar chart of the last 20 countries with a total population in 2021")+
  geom_text(aes(label=Population),size=4,hjust=-0.1)+
  ylab('Country')+
  xlab('Population')+
  ylim(0,50000)+
  coord_flip()+
  labs(fill="")+
  scale_fill_manual(values = c('中间国家' = "grey80", '后十名国家' ="blue"))+
  theme(legend.position = c(0.8,0.2),
        axis.title = element_text(size=20,face="plain",color="black"),
        axis.text = element_text(color = "black"),
        panel.background=element_rect(fill="white",colour=NA))
        
p2


#前20名国家柱形图制作
df3 <- df1[df1$rank >= 204,]
m3 = max(df3$Population)
p3 <- ggplot(data=df3,aes(x = Country_name,y = Population,fill = x))+
  geom_bar(stat = "identity")+
  ggtitle("Bar chart of the top 20 countries with a total population in 2021")+
  geom_text(aes(label=Population),size=4,hjust=-0.1)+
  ylab('Country')+
  xlab('Population')+
  ylim(0,m*1.2)+
  coord_flip()+
  labs(fill="")+
  scale_fill_manual(values = c('中间国家' = "grey80", '前十名国家' ="red"))+
  theme(legend.position = c(0.8,0.2),
        axis.title = element_text(size=20,face="plain",color="black"),
        axis.text = element_text(color = "black"),
        panel.background=element_rect(fill="white",colour=NA))
        # ,
        # panel.grid.major = element_line(colour = "grey80",size=0.25,linetype ="dotted" ),
        # panel.grid.minor = element_line(colour = "grey80",size=0.25,linetype ="dotted" ))
p3



