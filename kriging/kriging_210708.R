#library(sp)
#library(gstat)
#library(rgdal)
#library(e1071)
#library(dplyr)
#library(lattice)
#library(ggplot2)
#library(raster)

#data import
setwd("C:/Users/haley/Dropbox/DATA_08/DATA_08")
sh193 <- read.csv ("PM25_mean_month.csv")
sh193  <- sh193 [!is.na(sh193$PM25), ]
is.na(sh193$PM25)
head(sh193,3)
names(sh193)[4] <- "LON"
names(sh193)[5] <- "LAT"
names(sh193)[3] <- "PM25"

sh193 <- sh193 %>% filter(year_month == c("Jan-20"))

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
LAT.range <- range(as.integer(sh193@coords[,2 ])) + c(0,0.5)
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
sh193.var <- variogram(PM25~1,sh193, cloud=F, cutoff=200, width=5)
sh193.var 
plot(sh193.var, col="black", pch=16,cex=1,
     xlab="Distance (km)",ylab="Semivariance",
     main=expression("Variogram model PM "[2.5]* "in Siheung"))

##Model fit 
#vgm(psill, model, nugget, range)
sh193.model<- fit.variogram(sh193.var,vgm("Gau",10))
plot(sh193.var,model=sh193.model, col="black", cex=1.3, lwd=0.5,lty=1,pch=20,
     xlab="Distance (km)",ylab="Semivariance",
     main=expression("Variogram model - PM"[2.5]))

# calculate kriging
sh193.kriged <- krige(PM25 ~ 1, sh193, sh193.grid, model=sh193.model)

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

#OP's original plot code, adapted here to include kriging data as geom_tile
  ggplot()+ theme_minimal() +
  geom_tile(data = myKrige, aes(x= LON, y= LAT, fill = pred)) +
  scale_fill_gradient2(name=bquote(atop("PM25", mu*g~m^-3)), 
                       high="red", mid= "plum3", low="blue", 
                       space="Lab", midpoint = median(myKrige$pred))  + 
  geom_map(data= myKorea, map= myKorea, aes(x=long,y=lat,map_id=id,group=group),
           fill=NA, colour="black") +
  geom_point(data=myPoints, aes(x=LON, y=LAT, fill=PM25), 
             shape=21, alpha=1,na.rm=T, size=3) +
  coord_cartesian(xlim= LON.range, ylim= LAT.range) +
  #scale_size(range=c(2,4))+
  labs(title= "PM25 Concentration around Siheung Area: Jan-20",
       x="Longitude", y= "Latitude")+
  theme(title= element_text(hjust = 0.5,vjust = 1,face= c("bold")))
  ggsave("figure_Jan-20.png", dpi=1000, dev='png')
