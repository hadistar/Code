getwd()
setwd("C:/Users/haley/R/useful_R_code/ANOVA")

install.packages("car") #Levene Test
install.packages("agricolae") #Duncan Test
install.packages("nparcomp") #비모수 다중비교
install.packages("pgirmess")

library(car)
library(agricolae)
library(nparcomp)
library(pgirmess)

# ANOVA 
# 서로 독립인 3개 이상의 모집단의 평균이 다른지/차이가 나는지를 통계적으로 분석

#자료: 질적자료(집단이 3개이상) 1개/ 양적자료 1개
#ex) 작업장내 공정(a,b,c)내의 농도 비교

#순서
#정규성-> ANOVA or None-Parameter Method-Post Hoc

# 1단계: 정규성 검정
#귀무가설: 정규분포를 따른다.
#대립가설: 정규분포를 따르지 않는다.
View(InsectSprays)
by(InsectSprays$count, InsectSprays$spray, shapiro.test)

# 2단계: Non Parameyter Method: Kruskal-Wallis Rank Sum Test
kruskal.test(count~spray, data=InsectSprays) #Y(양적) ~ group(질적/집단), data 

#3단계: (비모수) 다중비교 (Multiple Comparsion) = 사후분석(Post_Hoc)
#nparcomp: Non-Parametric Method : Multiple Comparsion
#Type: Tykey(보수), Duncan(진보)

a <- nparcomp::nparcomp(count ~ spray,
                   data = InsectSprays,
                   type="Tukey")
a
# 정규성 가정 만족, 등분산 깨짐=이분산 만족
insect.anova <- oneway.test(count ~ spray,
                            data= InsectSprays,
                            var.equal = FALSE)

insect.anova

#결과보기

insect.anova <- aov(count ~ spray, data= InsectSprays)
summary(insect.anova)

#4단계: 다중비교(Multiple Comparsion) = 사후분석(Post-Hoc)
#조건: 1단계 정규성 만족, 3단계의 결론이 대립가설(집단간의 차이가 있어야함)

TukeyHSD(insect.anova)

a <- agricolae::duncan.test(insect.anova,
                       "spray",
                       alpha=0.05,
                       console = TRUE)
a
#e값 안나오게 하는법
options(scipen = 100)