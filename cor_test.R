# Correlation Test

#귀무가설: 두 양적자료간의 관련성(직선성=선형성)이 없다.
#대립가설: 두 양적 자료간의 관련성이 있다.


## 예제 1: cars(speed.dist)
#순서: 정규성 -> cor or 비모수

#귀무가설 : speed와 dist간에는 관련성이 없다.
#대립가설 : speed와 dist간에는 관련성이 있다.


#1단계: 정규성 검정
#귀무가설: 정규분포를 따른다.
#대립가설: 정규분포를 따르지 않는다.

shapiro.test(cars$speed)
shapiro.test(cars$dist)

#2단계 Kendall, Spearman의 비모수
# 정규성 가정이 깨졌거나, 자료가 순서형(순위형)일때 사용
# Spearson 은 질적자료에만 사용
# 검정력은 Pearson이 뛰어남
cor.test(cars$speed, cars$dist, method="kendall") 
cor.test(cars$speed, cars$dist, method="spearman") 

#2단계 정규성이 만족되었다면
cor.test(cars$speed, cars$dist, method="pearson")


## 예제 2: attitude

psych::corr.test(attitude, method="pearson")
attitude.corr.test <- psych::corr.test(attitude, method="pearson")
str(attitude.corr.test)
attitude.corr.test$r
round(attitude.corr.test$r, digits=3)
round(attitude.corr.test$p, digits=3)
result <- rbind(round(attitude.corr.test$r, digits=3),
                round(attitude.corr.test$p, digits=3))
result                
