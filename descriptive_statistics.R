# 예제파일 불러일들이기
#ggplot2는 본래 시각화 패키지임
#ggplot2 함수에 내장된 diamonds 데이터 불러오기
#install.packages("ggplot2")

library(ggplot2)
View(diamonds)

# dplyr 함수 설치(install.packages) 및 불러오기(library)
# install.packages("dplyr")
library(dplyr)

#class라는 변수명, 1~53940 숫자 리스트 생성
no <- c(1:53940)

dim(diamonds) # dim -> 차원
#data.frame 함수는 nxm 행렬(데이터)를 생성
d <- data.frame(no,diamonds)

#데이터 형식을 파악하는 다양한 방법들
summary(d) #데이터 요약
head(d) #데이터의 앞부분만
tail(d) #데이터의 뒷부분만
View(d) #데이터를 창에 띄워줌(가장많이씀)
dim(d) #내 데이터를 (nxm)로 보여줌

levels(d$cut)


d %>%
  summarise(n         = n(),
            GM        = mean(carat),
            AM        = exp(mean(log(carat))),
            TrimmedMean = mean(carat, trim = 0.05),
            Median      = median(carat),
            Range       = diff(range(carat)),
            IQR         = IQR(carat),
            VAR         = var(carat),
            SD          = sd(carat),
            GSD         = exp(sd(log(carat))),
            min         = min(carat),
            max         = max(carat))

d %>%
      group_by(clarity) %>%
      summarise(n         = n(),
                GM        = mean(depth),
                AM        = exp(mean(log(carat))),
                TrimmedMean = mean(depth, trim = 0.05),
                Median      = median(depth),
                Range       = diff(range(depth)),
                IQR         = IQR(depth),
                VAR         = var(depth),
                SD          = sd(depth),
                GSD         = exp(sd(log(depth))),
                min         = min(depth),
                max         = max(depth))

d %>%
  summarise(n         = n(),
            GM        = mean(carat),
            SD          = sd(carat),
            AM        = exp(mean(log(carat))),
            GSD         = exp(sd(log(carat))),
            min         = min(carat),
            max         = max(carat))


ex <- d%>% filter(clarity=="I1")
          