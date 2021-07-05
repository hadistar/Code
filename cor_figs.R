getwd()
setwd("C:/Users/haley/R/useful_R_code/cor_test")

#패키지 설치 및 로딩
#install.packages("corrplot")
#install.packages("car")
#install.packages("rgl")
#install.packages("psych")

library(corrplot)
library(car)
library(rgl)
library(ggplot2)
library(psych)
library(writexl)

#Correlation Analysis 상관분석
#두개의 양적자료간의 선형성을 통계적으로 분석하는 방법
# 원인과 결과의 관계(인과관계) 아님

## 1) Scatter plot using basic
#예제: cars -> Speed(속도)-dist(제동거리)

plot(cars$speed, cars$dist, col="red")

## 2-1) scatter plot using ggplot2
View(mtcars)
p <- ggplot(data=mtcars,aes(x=wt,y=mpg))
p1 <- p + geom_point(aes(col="red")) + theme_classic() 
p2 <- p1 + labs(title = "Scatter Plot using ggplto2",
                    x = "Weight of Car",
                    y = "Mile Per Gallon")+ 
            theme(plot.title = element_text(size=30),
                 axis.title.x = element_text(size = 20),
                 axis.title.y = element_text(size = 20))
p3 <- p2 + facet_wrap(~cyl)
p3

## 2-2)
View(mtcars)
p <- ggplot(data=mtcars,mapping = aes(x=wt,y=mpg, col=cyl, size= cyl))
p1 <- p + geom_point() + theme_classic()
p2 <- p1 + labs(title = "Scatter Plot using ggplto2",
                x = "Weight of Car",
                y = "Mile Per Gallon")+ 
  theme(plot.title = element_text(size=20),
        axis.title.x = element_text(size = 10),
        axis.title.y = element_text(size = 10))
p2

## 3-1) SPM(Scatter Plot Matrix)
plot(attitude)
plot(iris[,1:4])
View(iris)
## 3-2) corrplot 이용
#https://rpubs.com/cardiomoon/27134
mtcars$cyl <- as.numeric(mtcars$cyl)
M <- cor(mtcars)
col <- colorRampPalette(c("#BB4444","#EE9988","#FFFFFF","#77AADD","#4477AA"))
corrplot(M,
         method= "color",
         col = col(200),
         type = "upper",
         order = "hclust",
         number.cex = .7,
         addCoef.col = "black",
         tl.col = "black",
         tl.srt = 90,
         sig.level = 0.01,
         insig = "blank",
         diag = FALSE)

## 4) #3D Scatter plot
#예제: car.rgl packages
scatter3d(x = iris$Sepal.Length,
          y = iris$Sepal.Width,
          z = iris$Petal.Length,
          groups = iris$Species,
          surface = FALSE,
          grid = FALSE,
          ellipsoid = TRUE)
