library(readr)
library(dplyr)
library(openxlsx)
library(data.table)

data <- read_csv("AirKora_2019_2020_SH_100km.csv")
data   <- data  [!is.na(data $PM25), ]
is.na(data $PM25)
dim(data)

setDT(data)[, month := format(as.Date(date), "%m") ]
setDT(data)[, year := format(as.Date(date), "%Y") ]
setDT(data)[, year_month := format(as.Date(date), "%Y-%m") ]
dim(data)

PM2.5_mean_day <- data %>% group_by(date,code) %>% summarize(PM25_mean = mean(PM25))
PM2.5_mean_month <- data %>% group_by(year_month,code) %>% summarize(PM25_mean = mean(PM25))
#d <- data[,c(2, 9:10)]
#md <- PM2.5_mean_day[,c(2)]
#md <- merge(md, d, by='code')
#cbind(PM2.5_mean_day,md)
head(PM2.5_mean_day)
head(PM2.5_mean_month)

write.xlsx(PM2.5_mean_day, sheetName="sheet1", file="PM2.5_mean_day.xlsx")
write.xlsx(PM2.5_mean_month, sheetName="sheet1", file="PM2.5_mean_month.xlsx")


