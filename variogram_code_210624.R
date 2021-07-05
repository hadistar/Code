#download the necessary packages
 #install.packages("sp")
 #install.packages("gstat")
 #install.packages
library(sp)
library(gstat)
library(rgdal)  
library(raster)
library(readr)

##specifying the path
 #checking the current path
getwd()
 #specifying the path :ex) setwd("your path")
setwd("C:/Users/haley/Dropbox/DATA_08/DATA_08")

##data import
train <- read_csv("seoul032823.csv")
train <- train[!is.na(train$PM25), ]
dim(train)
View(train)

##assign a CRS(Coordinate Reference Systems) and reproject
 #WGS(World Geodetic System) -> geographic longitude and latitude
from_crs = CRS("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")
 #convert to TM(Transverse Mercator)
to_crs = CRS("+proj=tmerc +lat_0=38 +lon_0=127 +k=1 +x_0=200000 +y_0=500000 +ellps=bessel +units=km")

coordinates(train)=~lon+lat
proj4string(train) <- from_crs
train2 <- spTransform(train, to_crs)

##plot semi-variogram
 #You can choose two versions.
 # 1. cloud=T // Plotting the variograms of all data pairs
 # 2.cloud=F //  Plotting only representative values
train.var <- variogram(PM25~lon+lat, train2, cloud=T, cutoff=150)
train.var 
plot(train.var, col="black", pch=16,cex=1,
     xlab="Distance (km)",ylab="Semivariance",
     main=expression("Variogram model PM "[2.5]* "in Siheung"))
##Model fit 
 #vgm(psill, model, nugget, range)
train.model<- fit.variogram(train.var,vgm(10,"Gau",10,100),fit.method = 2)
plot(train.var,model=train.model, col="black", cex=1.3, lwd=0.5,lty=1,pch=20,
     xlab="Distance (km)",ylab="Semivariance",
     main=expression("Variogram model for 6 sites - PM"[2.5]))


