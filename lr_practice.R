getwd()
setwd("C:/Users/haley/R/useful_R_code/regression")

# data import
d <- read.csv("data.salary.txt")

#데이터 확인
View(d)
dim(d)
summary(d)
head(d)
tail(d)

library(ggplot2)
ggplot(d,aes(x=X,y=Y))+geom_point()+geom_smooth(method='lm')+theme_classic()

# lm 함수 이용하여 추정
res_lm <- lm(Y ~ X,data=d)

#결과 확인
#결과 해석// 절편 a: -1197 기울기 b: 219 -> 나이를 한살 먹을때마다 연봉 219씩 증가
summary(res_lm)

#매개변수의 신뢰구간 및 새로운 데이터 예측구간 생성

X_new <- data.frame(X=23:60) #예측하고싶은 연봉 데이터
View(X_new)
# 신뢰구간
conf_95 <- predict(res_lm, X_new, interval='confidence', level=0.95)
conf_95_d <- data.frame(X_new, conf_95)
conf_50 <- predict(res_lm, X_new, interval='confidence', level=0.50)
conf_50_d <- data.frame(X_new, conf_50)

age50_conf <- subset(conf_95_d, X_new==50)

#예측구간
pred_95 <- predict(res_lm, X_new, interval='prediction', level=0.95)
pred_95_d <- data.frame(X_new, pred_95)
pred_50 <- predict(res_lm, X_new, interval='prediction', level=0.50)
pred_50_d <- data.frame(X_new, pred_50)

age50_pred <- subset(pred_95_d, X_new==50)

# fig 
library(ggplot2)

# fig 신뢰구간
c <- ggplot()
c1 <- c + theme_bw(base_size=18)
c2 <- c1 + geom_ribbon(data=conf_95_d, aes(x=X, ymin=lwr, ymax=upr), alpha=1/6)
c3 <- c2 + geom_ribbon(data=conf_50_d, aes(x=X, ymin=lwr, ymax=upr), alpha=2/6)
c4 <- c3 + geom_line(data=conf_50_d, aes(x=X, y=fit), size=1)
c5 <- c4 + geom_point(data=d, aes(x=X, y=Y), shape=1, size=3)
c6 <- c5 + labs(x='X', y='Y') + coord_cartesian(xlim=c(22, 61), ylim=c(2000, 14000))
c7 <- c6 + scale_y_continuous(breaks=seq(from=2000, to=14000, by=4000))
c7

# fig 예측구간
p <- ggplot()
p1 <- p + theme_bw(base_size=18)
p2 <- p1 + geom_ribbon(data=pred_95_d, aes(x=X, ymin=lwr, ymax=upr), alpha=1/6)
p3 <- p2 + geom_ribbon(data=pred_50_d, aes(x=X, ymin=lwr, ymax=upr), alpha=2/6)
p4 <- p3 + geom_line(data=pred_50_d, aes(x=X, y=fit), size=1)
p5 <- p4 + geom_point(data=d, aes(x=X, y=Y), shape=1, size=3)
p6 <- p5 + labs(x='X', y='Y') + coord_cartesian(xlim=c(22, 61), ylim=c(2000, 14000))
p7 <- p6 + scale_y_continuous(breaks=seq(from=2000, to=14000, by=4000))
p7
