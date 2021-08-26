library(sp)
library(gstat)
library(rgdal)
library(e1071)
library(dplyr)
library(lattice)
library(ggplot2)
library(raster)

# 고농도 순으로 짜름
#sh193 <- read.csv ("AirKora_2019_2020_SH_100km.csv")
#sh193 <- sh193 %>% filter(code == c("131231"))
#sh193 <- sh193[,c(1:2, 8:10)]
#sh193 <- sh193 %>% filter(PM25>=76)
#sh193$PM25 <- sort(sh193$PM25,decreasing=T)
# write.csv(sh193,"siheung_PM25_very_bad.csv")

# 고농도 순으로 짜름
# sh193$PM25 <- sort(sh193$PM25,decreasing=T)
# head(sh193,10)
# View(sh193)

#data import
getwd()
setwd("D:/GitHub/Code/kriging")
sh193 <- read.csv ("AirKora_2019_2020_SH_100km.csv")
sh193  <- sh193 [!is.na(sh193$PM25), ]
sh193 <- sh193[,c(1:2, 7:10)]
is.na(sh193$PM25)
head(sh193,3)
names(sh193)[5] <- "LAT"
names(sh193)[6] <- "LON"
names(sh193)[4] <- "PM25"

sh193$PM25 <- log(sh193$PM25)

sh193 <- sh193 %>% filter(date == c("2020-12-11"))

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
#sh193 <- spTransform(sh193, CRS("+proj=utm +north +zone=52 +datum=WGS84"))

#Creating the grid for Kriging
LON.range <- range(as.integer(sh193@coords[,1 ])) + c(0,1)
LAT.range <- range(as.integer(sh193@coords[,2 ])) + c(0.25,0.25)
sh193.grid <- expand.grid(LON = seq(from = LON.range[1], to = LON.range[2], by = 0.02),
                          LAT = seq(from = LAT.range[1], to = LAT.range[2], by = 0.02))

plot(sh193.grid)
points(sh193, pch= 16,col="red")
coordinates(sh193.grid)<- ~LON+LAT
proj4string(sh193.grid) <- "+proj=longlat +datum=WGS84" 
gridded(sh193.grid)<- T
plot(sh193.grid)
points(sh193, pch= 16,col="red")

# calculate kriging
# create variogram
#sh193.var <- variogram(PM25~LAT+LON,sh193, cloud=F, cutoff=200, width=5,alpha=c(0,45,90,135,180))
sh193.var <- variogram(PM25~LAT+LON,sh193, cloud=F, cutoff=200, width=5)
sh193.var 
plot(sh193.var, col="black", pch=20,cex=1,
     xlab="Distance (km)",ylab="Semivariance",
     main=expression("Variogram model- PM "[2.5]* "for Siheung, 2020-12-11"))

##Model fit 
#vgm(psill, model,range, nugget)
sh193.model<- fit.variogram(sh193.var,vgm(1, "Mat", 1, 1, kappa=0.3))
plot(sh193.var,model=sh193.model, col="black", cex=1, lwd=0.5,lty=1,pch=20,
     xlab="Distance (km)",ylab="Semivariance",
     main=expression("Variogram model- PM "[2.5]* "for Siheung, 2020-12-11"))


# calculate kriging
sh193.kriged <- krige(PM25 ~LAT+LON, sh193, sh193.grid, model=sh193.model)

# Reprojection of skorea into same coordinates as sp objects
coordinates(skorea) <- ~long+lat  #{sp} Convert to sp object
proj4string(skorea) <- "+proj=longlat +datum=WGS84" #{sp} set projection attributes


#Convert spatial objects into data.frames for ggplot2
myPoints <- data.frame(sh193)
myKorea <- data.frame(skorea)
#Extract the kriging output data into a dataframe.  
#This is the MAIN PART!
myKrige <- data.frame(sh193.kriged@coords, 
                      pred = sh193.kriged@data$var1.pred)  
str(sh193.kriged)


#Preview the data
head(myKrige, 10)

#     LON     LAT     pred
#1 290853 4120600 167.8167
#2 292353 4120600 167.5182
#3 293853 4120600 167.1047
myKrige$pred <- exp(myKrige$pred)
#OP's original plot code, adapted here to include kriging data as geom_tile
ggplot()+ theme_minimal() +
  geom_tile(data = myKrige, aes(x= LON, y= LAT, fill = pred)) +
  scale_fill_gradient2(name=bquote(atop(PM[2.5], mu*g/m^3)), 
                       high="red", mid= "plum3", low="blue", 
                       space="Lab", midpoint = median(myKrige$pred))+
  geom_map(data= myKorea, map= myKorea, aes(x=long,y=lat,map_id=id,group=group),
           fill=NA, colour="black") +
  geom_point(data=myPoints, aes(x=LON, y=LAT, fill=exp(PM25)), 
             shape=21, alpha=1,na.rm=T, size=3) +
  coord_cartesian(xlim= LON.range, ylim= LAT.range) +
  #scale_size(range=c(2,4))+
  labs(title=expression('PM'['2.5 ']*'Concentration around Siheung Area: 2020-12-11'),
       x="Longitude", y= "Latitude")+
  theme(title= element_text(hjust = 0.5,vjust = 1,face= c("bold")))
ggsave("figure_2020-12-11.png", dpi=1000, dev='png')
