library(maps)
library(ggplot2)
library(RColorBrewer)
library(dplyr)
u = getwd()
setwd(u)

colormap<-c(brewer.pal(9,"YlOrRd")[c(2,3,4,5,6,7,8,9)])
df <- read.csv("各国人口（降序）.csv",header=TRUE,stringsAsFactors = FALSE)
df1 <- arrange(df, Population)
df1$rank <- c(1:223)
df1$x <- ifelse(df1$rank <= 10, "后十名国家", ifelse(df1$rank >= 214, "前十名国家", "中间国家"))
df1$Country_name<-factor(df1$Country_name,levels = unique(df1$Country_name),ordered = T)
world_map <- map_data("world")




#排名前10个国家地理图制作
mydata2 <- df1[df1$rank >= 214,]
mydata2$C <- as.vector(mydata2$Country_name)
mydata2$C[mydata2$C == 'United States'] <- 'USA'

mydata2$b<-mydata2$Population/100000000
mydata2$fan<-cut(mydata2$b,
                breaks=c(0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,15),
                labels=c("0~0.5","0.5~1","1~1.5","1.5~2","2~2.5",
                         "2.5~3","3~3.5",">3.5"),
                order=TRUE)

ggplot()+
  geom_map(data=mydata2,aes(map_id=C,fill=fan),map=world_map)+
  geom_path(data=world_map,aes(x=long,y=lat,group=group),colour="black",linewidth=0.2)+
  coord_map("mercator",xlim=c(-180,180), ylim=c(-90, 90))+ #墨卡托投影
  scale_y_continuous(breaks=(-3:3)*30) +
  scale_x_continuous(breaks=(-6:6)*30) +
  ylab("")+
  xlab("")+
  scale_fill_manual(name="one hundred million persons",values= colormap,na.value="grey75")+
  guides(fill=guide_legend(reverse=TRUE)) +
  theme_minimal()









