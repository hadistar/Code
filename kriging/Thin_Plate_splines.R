# TPS: Thin-Plate splines -------------------------------------------------

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


#calculate TPS
surf.1<-Tps(Koreapred$coords,Koreapred$Mean_PM25)
head(surf.1,5)

summary(Koreapred)
#calculate grid
predlon <- seq(min(Koreapred$lon)-0.1,max(Koreapred$lon)+0.1,,200)
predlat <- seq(min(Koreapred$lat)-0.1,max(Koreapred$lat)+0.1,,200)
summary(predlat)


#Adjust the lat&lon value to zoom on the map
LON.range <- as.integer(matrix(c(min(predlon),max(predlon)),nrow=1))
LAT.range <- as.integer(matrix(c(min(predlat),max(predlat)),nrow=1))

#expand to grid
Koreagrid <- expand.grid(predlon,predlat)
names(Koreagrid) <- c("lon", "lat")
head(Koreagrid)

#krig
surf.1.pred<-predict.Krig(surf.1,Koreagrid)
head(surf.1.pred,5)

#predict value + lat,lon
data <- cbind(Koreagrid,surf.1.pred)
head(data,5)


# plotting using sp package -----------------------------------------------
# require(sp)
# plot(Koreagrid,pch=20,asp=1,cex=.6,col=bpy.colors(256)[cut(surf.1.pred,256)],
#             xlab="Longitude",ylab="Latitude",main="Korea PM2.5")
# grid(col="gray")


# plotting using ggplot2 package ------------------------------------------

#import map
library(raster)
skorea<- getData("GADM", country= "KOR", level=2)
skorea<- fortify(skorea)
skorea <- data.frame(skorea)


library(ggplot2)
tsp_fig <- ggplot()+ theme_minimal() +
  geom_tile(data = data, aes(x= lon, y= lat, fill = surf.1.pred)) +
  scale_fill_gradient2(name=bquote(atop(PM[2.5], mu*g/m^3)),
                       low = "blue", high = "red",
                       mid = "white", midpoint=median(data$surf.1.pred))+
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
