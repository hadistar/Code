# TPS: Thin-Plate splines -------------------------------------------------

# install.packages("readxl")
# install.packages("fields")
# install.packages("spam")
# install.packages("maps")

library(readxl)
require(fields)
require(spam)
require(grid)
require(maps)
require(gstat)
library(ggplot2)
getwd()
setwd("D:/GitHub/Code/kriging")
# setwd("C:/Users/e-park/Dropbox/My DropBox/Maps/Korea data/MMRA on Korea PM25")
# -------------------------------------------------------------------------

# data import
Koreapred <- read.csv("PM25_avg_over_days.csv")
Koreapred$coords<-matrix(c(Koreapred$lon,Koreapred$lat),byrow=F,ncol=2)
# str(Koreapred$coords)
surf.1<-Tps(Koreapred$coords,Koreapred$Mean_PM25)
head(surf.1)
# class(surf.1)
# summary(surf.1)
# print(surf.1$lambda)

#Creating the grid 
predlon <- seq(min(Koreapred$lon)-0.1,max(Koreapred$lon)+0.1,,200)
predlat <- seq(min(Koreapred$lat)-0.1,max(Koreapred$lat)+0.1,,200)
Koreagrid <- expand.grid(predlon,predlat)
names(Koreagrid) <- c("lon", "lat")
head(Koreagrid)
# predlocs <- cbind(predlocs1$Var1,predlocs1$Var2)
#y.pred <- rep(NA,nrow(predlocs))

#Koreagrid<-matrix(c(dataplot[,1],dataplot[,2]),byrow=F,ncol=2) 
surf.1.pred<-predict.Krig(surf.1,Koreagrid)
summary(surf.1.pred)
# summary(as.vector(surf.1.pred))

# surf.1.pred.m<-matrix(surf.1.pred,length(Koreagrid[,1]),length(Koreagrid[,2]),byrow=F)
# str(surf.1.pred.m)
data <- cbind(Koreagrid,surf.1.pred)
head(data,5)


# plotting using sp package -----------------------------------------------
# require(sp)
# 
# plot(Koreagrid,pch=20,asp=1,cex=.6,col=bpy.colors(256)[cut(surf.1.pred,256)],
#             xlab="Longitude",ylab="Latitude",main="Korea PM2.5")
# 
# grid(col="gray")
library(raster)
skorea<- getData("GADM", country= "KOR", level=2)
skorea<- fortify(skorea)
skorea <- data.frame(skorea)
#require(ggplot2)
# plotting using ggplot2 package ------------------------------------------
library(ggplot2)
tsp_fig <- ggplot()+ theme_minimal() +
  geom_tile(data = data, aes(x= lon, y= lat, fill = surf.1.pred)) +
  scale_fill_gradient2(name=bquote(atop(PM[2.5], mu*g/m^3)),
                       low = "blue", high = "red",
                       mid = "white", midpoint=22.32)+
  geom_map(data= skorea, map= skorea, aes(x=long,y=lat,map_id=id,group=group),
           fill=NA, colour="black") +
  coord_cartesian(xlim= LON.range, ylim= LAT.range) +
  theme(panel.grid = element_line(color = "grey", linetype="dashed", size=0.2),
        panel.ontop = TRUE, panel.background = element_rect(color = NA, fill = NA))+
  labs(title=expression(''),
       x="Longitude", y= "Latitude")+
  theme(title= element_text(hjust = 0.5,vjust = 1,face= c("bold")))+
  theme(axis.text.x = element_text(face= c("bold")),axis.text.y = element_text(face= c("bold")))
tsp_fig
ggsave("tsp_fig.png", dpi=1000, dev='png')
