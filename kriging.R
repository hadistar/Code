#install.packages("automap")
#install.packages("e1071")
#install.packages("lattice")

library(sp)
library(gstat)
library(automap)
library(rgdal)
library(e1071)
library(dplyr)
library(lattice)
library(sp)
library(gstat)
library(automap)
library(rgdal)
library(e1071)
library(dplyr)
library(lattice)
library(ggplot2)
library(raster)


setwd("C:/Users/haley/Dropbox/DATA_08/DATA_08")
sh193 <- read.csv ("AirKora_2019_2020_SH_100km_20200624.csv")
sh193  <- sh193 [!is.na(sh193$PM25), ]
is.na(sh193$PM25)

#plotting the PM25 data on Korea Map
skorea<- getData("GADM", country= "KOR", level=2)
plot(skorea)
skorea<- fortify(skorea)
ggplot()+
  geom_map(data= skorea, map= skorea, aes(x=long,y=lat,map_id=id,group=group),
           fill=NA, colour="black") +
  geom_point(data=sh193, aes(x=LON, y=LAT), 
             colour= "red", alpha=0.7,na.rm=T) +
  labs(title= "PM25 Concentration in Siheung Area at South Korea",
       x="Longitude", y= "Latitude", size="PM25(microgm/m3)")+
  theme(title= element_text(hjust = 0.5,vjust = 1,face= c("bold")))

# Reprojection
coordinates(sh193) <- ~LON+LAT
proj4string(sh193) <- "+proj=longlat +datum=WGS84" 
sh193 <- spTransform(sh193, CRS("+proj=utm +north +zone=52 +datum=WGS84"))

#Creating the grid for Kriging
LON.range <- range(as.integer(sh193@coords[,1 ])) + c(0,1)
LAT.range <- range(as.integer(sh193@coords[,2 ]))
sh193.grid <- expand.grid(LON = seq(from = LON.range[1], to = LON.range[2], by = 1800),
                                LAT = seq(from = LAT.range[1], to = LAT.range[2], by = 1800))
plot(sh193.grid)
points(sh193, pch= 16,col="red")
coordinates(sh193.grid)<- ~LON+LAT
gridded(sh193.grid)<- T
plot(sh193.grid)
points(sh193, pch= 16,col="red")

# kriging spatial prediction
sh193_OK<- autoKrige(formula = PM25~1,input_data = sh193, new_data = sh193.grid )

# Reprojection of skorea into same coordinates as sp objects
coordinates(skorea) <- ~long+lat  #{sp} Convert to sp object
proj4string(skorea) <- "+proj=longlat +datum=WGS84" #{sp} set projection attributes
#{sp} Transform to new coordinate reference system
#skorea <- spTransform(skorea, CRS("+proj=utm +north +zone=52 +datum=WGS84")) 

#Convert spatial objects into data.frames for ggplot2
myPoints <- data.frame(sh193)
myKorea <- data.frame(skorea)
#Extract the kriging output data into a dataframe.  
#This is the MAIN PART!
myKrige <- data.frame(sh193_OK$krige_output@coords, 
                      pred = sh193_OK$krige_output@data$var1.pred)   
#Preview the data
head(myKrige, 3)
#     LON     LAT     pred
#1 290853 4120600 167.8167
#2 292353 4120600 167.5182
#3 293853 4120600 167.1047

#######################################
#Reproject the krige data
myKrige1 <- myKrige
coordinates(myKrige1) <- ~LON+LAT 
proj4string(myKrige1) <-"+proj=utm +north +zone=52 +datum=WGS84" 
myKrige_new <- spTransform(myKrige1, CRS("+proj=longlat")) 
myKrige_new <-  data.frame(myKrige_new@coords, pred = myKrige_new@data$pred) 
LON.range.new <- range(myKrige_new$LON) 
LAT.range.new <- range(myKrige_new$LAT)

#Original data have correct lat/lon data
sh193_1 <- read.csv ("AirKora_2019_2020_SH_100km_20200624.csv")
sh193_1  <- sh193_1[!is.na(sh193_1$PM25),]
dim(sh193_1)

#Original skorea data transformed the same was as myKrige_new
skorea1 <- getData("GADM", country= "KOR", level=2)
skorea1
#Convert SpatialPolygonsDataFrame to dataframe (deprecated.  see `broom`)
skorea1 <- fortify(skorea1)  
coordinates(skorea1) <- ~long+lat  #{sp} Convert to sp object
proj4string(skorea1) <- "+proj=longlat +datum=WGS84" #{sp} set projection attributes 1
#{sp} Transform to new coordinate reference system
myKorea1 <- spTransform(skorea1, CRS("+proj=longlat")) 
myKorea1 <- data.frame(myKorea1)  #Convert spatial object to data.frame for ggplot

ggplot()+
  stat_summary_2d(data=myKrige_new, aes(x = LON, y = LAT, z = pred),
                  binwidth = c(0.05,0.05)) +
  scale_fill_gradient2(name=bquote(atop("PM25", mu*g~m^-3)), 
                       high="red", mid= "plum3", low="blue", 
                       space="Lab", midpoint = median(myKrige_new$pred)) +
  geom_map(data= myKorea1, map= myKorea1, aes(x=long,y=lat,map_id=id,group=group),
           fill=NA, colour="black") +
  geom_point(data= sh193_1, aes(x=LON, y=LAT, fill=PM25), 
             shape=21, alpha=1,na.rm=T, size=4) +
  coord_cartesian(xlim= LON.range.new, ylim= LAT.range.new) +
  #scale_size(range=c(2,4))+
  labs(title= "PM25 Concentration in Siheung Area at South Korea",
       x="Longitude", y= "Latitude")+
  theme(title= element_text(hjust = 0.5,vjust = 1,face= c("bold")))

