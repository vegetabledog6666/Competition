library(ggplot2)
df<-read.csv("Japan2.csv")
df1<-read.csv("Brazil2.csv")
df2<-read.csv("Russia2.csv")
df_melt<-melt(df,id="Year")
df_melt1<-melt(df1,id="Year")
df_melt2<-melt(df2,id="Year")
a<-ggplot(df_melt, aes(x=Year, y=value, group=variable)) +
  geom_area(stat="identity",position="stack",aes(fill=variable)) +
  labs(x = "Year",y = "")+
  scale_fill_brewer(palette = 7)+
  theme(legend.position = "bottom",
        plot.title = element_text(hjust = 0.5))+
  ggtitle("Japan")
b<-ggplot(df_melt1, aes(x=Year, y=value, group=variable)) +
  geom_area(stat="identity",position="stack",aes(fill=variable)) +
  labs(x = "Year",y = "Proportion")+
  scale_fill_brewer(palette = 4)+
  theme(legend.position = "bottom",plot.title = element_text(hjust = 0.5))+
  ggtitle("Brazil")
c<-ggplot(df_melt2, aes(x=Year, y=value, group=variable)) +
  geom_area(stat="identity",position="stack",aes(fill=variable)) +
  labs(x = "Year",y = "")+
  scale_fill_brewer(palette = 3)+
  theme(legend.position = "bottom",plot.title = element_text(hjust = 0.5))+
  ggtitle("Russia")
Rmisc::multiplot(b,c,a,cols=3)