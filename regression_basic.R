#Regression Analysis
#어떤 양적자료가 다른 양적자료에게 영향을 주는지 => 인과관계(원인과 결과의 관계)

#Prediction and Classification
#ex) share; stock or time seires

#Simple Linear Regerssion Analysis
#반응변수(종속변수) = 설명변수(독립변수)

# result <- lm(y~x, data=) // lm= linear model
#summary(result)
View(cars)
cars.lm <- lm(dist~speed, data=cars)
summary(cars.lm)

###결과해석
## 1단계 
#귀무가설: 회귀모형은 타당하지 않다.
#대립가설: 회귀모형은 타당하다.

## 2단계
#귀무가설: 설명변수가 반응변수에 영향 주지않는다
#대립가설: 설명변수가 반은변수에 영향을 줄것이다.
#설명변수가 반응변수에 영향을 주는지?
#조건: 회귀모델이 타당할것.

## 3단계
#설명변수가 반응변수에 어떠한 영향을?
# y(dist) = aX+b+e  e ~ N(0, simag)
# y(dis)  =  3.9424 X - 17.5791

##4단계
#회귀모형의 설명력 = 설명변수의 설명력
#설명변수가 종속변수의 다름을 어느정도 설명? // 속도가 제동거리에 영향을 주는것을 65% 설명할수 있다.

## 5단계 predictrion
#predict(model, newdata=data.frame(독립변수=))
#model =lm 진행한모델
#설명변수를 바꿔서 예측해보는것.

predict(cars.lm, newdata=data.frame(speed=200))

predict(cars.lm, newdata=data.frame(speed=c(100,200,300)))

#training, test data로 나누기
install.packages("caret")
library(caret)
cars.index <- caret::createDataPartition(cars$speed,p=0.8)
cars.train <-cars[unlist(cars.index),]
cars.test <-cars[-unlist(cars.index),]

cars.train.lm <- lm(dist~speed, data=cars.train)
summary(cars.test.lm)

cars.predict <- predict(cars.train.lm, newdata=cars.test)
cars.predict

#MSE 구하기
#MSE: 값들이 각각의 그룹의 평균에서 얼마나 떨어져 있는지 확인(분산)
#mean(sum(실제값-예측값**2))
mean((cars.test$dist-cars.predict)**2)
