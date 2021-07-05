getwd()
setwd("C:/Users/haley/R/useful_R_code/descriptive_statistics")
#---------------------------------------------------------------------------------------
#독립표본 t-test: 서로 다른 두개의 그룹간의 평균 비교
#대응표본 t-test: 하나의 집단에 대한 비교
#단일표본 t-test: 특정 집단의 평균이 어떤 숫자와 같은지 다른지 비교

# mux1=mux2: 양측검정
# mux1>mux2: 단측검정

#---------------------------------------------------------------------------------------
# alt     two.sided(양측검정)                    Less(단측검정); x1이 작은경우
#var.eaual=T
#        t.test(x,y,var.eaual=T,alt='two.sided')  t.test(x1,y2,var.eaual=T,alt='less')
#var.eaual=F
#        t.test(x,y,var.eaual=F,alt='two.sided')  t.test(x,y,var.eaual=F,alt='less')
#---------------------------------------------------------------------------------------
#※등분산 가정안하면 welch test (유의확률 높아짐)





# 1)one sample t-test###########################################################
#한 변수의 평균을 특정값과 비교
#데이터 적용: 하나의 모집단이 이전보다 커졌냐? 작아젔냐?

#가설)
# 귀무가설: 성인들의 평균키는 168cm 임 (증명하기 힘든것) p-value > 0.05
# 대립가설: 성인들의 평균키는 168cm 보다 크다 p-value < 0.05

#Step1 정규성 검정: Shapiro-wlilk's
# 귀무가설: 성인들의 키는 정규분포를 따른다
# 대립가설: 따르지 않는다.

height.normal <-shapiro.test(body$height)
height.normal

#step 2-1 one sample t.test
one.ttest <-t.test(body$height, mu=168, arg = "greater")
one.ttest

#step 2-2 WIlcoxon's signed rank test (정규성 x)

wilcox.test(body$height, mu=168, arg = "greater" )

# if- else문
height.normal$statistic
height.normal$p.value

if(height.normal$p.value >= 0.05){
    t.test(body$height, 
            mu= 168,
           arg="greater")
}else{
  wilcox.test(body$height, mu=168, arg = "greater")

}

# if- else문(결과 모두 보기를 원한다면?)

height.normal <-shapiro.test(body$height)
test.statistics <- c()
pvalue <- c()

if(height.normal$p.value >= 0.05){
  print("#one sample t-test #")
  result <- t.test(body$height, 
         mu= 168,
         arg="greater")
  test.statistics <-result$statistic
  pvlaue <- result$p.value
}else{
  print("#Wilcoxon's signed rank test #")
  result <- wilcox.test(body$height, 
                        mu=168, 
                        arg = "greater")
  test.statistics <-result$statistic
  pvlaue <- result$p.value
}

#나는 한꺼번에 하겠다. 
t.method <- c()
t.statistic <- c()
t.pvalue <- c()
t.mu <-c(168, 65, 100) #
t.alternative <- c("greater","less","two.sided")

for(i in 2:4){#
  norm.test <- shapiro.test(unlist(body[,i]))
  #데이터 프레임은 I x J열 구조라, 벡터로 변환하여 인덱싱
  
 if(norm.test$p.value>=0.05){
   t.test.result <- t.test(unlist(body[,i]),#
                           mu = t.mu[i-1],
                           arg = t.alternative[i-1])
   
   t.method <- c(t.method, t.test.result$method)
   t.statistic <- c(t.statistic,t.test.result$statistic)
   t.pvalue <- c(t.pvalue, t.test.result$p.value)
 }else{
   wilcox.test.result <- wilcox.test(unlist(body[,i]),#
                                     mu = t.mu[i-1],
                                     arg = t.alternative[i-1])
   t.method <- c(t.method, wilcox.test.result$method)
   t.statistic <- c(t.statistic, wilcox.test.result$statistic)
   t.pvalue <- c(t.pvalue, wilcox.test.result$p.value)
 }
}

resultDF1 <- data.frame(Variable = colnames(body)[2:4],
                        Method   = t.method,
                        Statistic= t.statistic,
                        Pvalue   = t.pvalue)

install.packages("writexl")
library(writexl)
writexl :: write_xlsx(resultDF1,
                      path = "one_t_test.xlsx")

#solving wilcox tie wanrnig
#install.packages("eaxctRankTests")
#library(eaxctRankTests)
#eaxctRankTests :: wilcox.exact(body$height,
                               #mu=168,
                               #arg= "less")

# 2)two sample t-test###########################################################
#두개의 독립적인 (모)집단의 평균이 다른지 통계적으로 알겠다.
#양적자료, 질적자료 1개(2개의 값으로 이루어진)

#순서
#1) 정규성
#2) 등분산검정
#3) two sample t-test


library(ggplot2)
install.packages("nortest")
library(nortest)
View(diamonds)

diamonds$cut.group <- ifelse(diamonds$cut =="Ideal",
                             "Ideal",
                             "Non-Ideal")

#귀무가설: Ideal과 Non-Ideal간에 Price에는 차이가 없다(mu1 = mu2)
#대립가설: Ideal의 평균이 Non-Ideal의 평균 price보다 높다 (mu1>mu2)


#Step1 정규성 검정: Anderson-Darling Test
# 귀무가설: 정규분포를 따른다
# 대립가설: 따르지 않는다.

nortest::ad.test(diamonds[diamonds$cut.group=="Ideal",]$price) #==
nortest::ad.test(diamonds[diamonds$cut.group!="Ideal",]$price) #!=
#or
by(diamonds$price, diamonds$cut.group, ad.test)

#2단계: Wilcoxon's rank sum test

wilcox.test(diamonds$price~diamonds$cut.group,  #wilcox.test(양적자료~질적자료) 
            alternative="greater")


#2-1단계:  만약 등분산 가정 성립?
t.test(diamonds$price~diamonds$cut.group,
       alternative="greater",
       var.equal= TRUE)

#total
colnames(diamonds)
T.method <-c()
T.equality <-c()    
T.statistic <-c()
T.pvalue <-c()

for(i in c(1, 5:10)){
  #1단계 정규성
  norm.test <- by(unlist(diamonds[, i]), diamonds$cut.group, ad.test)
  
  #1단계가 만족될 경우
if ((norm.test$Ideal$p.value >= 0.05) & (norm.test$'Non-Ideal'$p.value>= 0.05)){
  #2단계 검정(등분산)  
  var.test.result <- var.test(unlist(diamonds[,i])~diamonds$cut.group)
   
if(var.test.result$p.value >= 0.05){
  #2단계가 만족할 경우
  t.test.result <- t.test(unlist(diamonds[,i])~diamonds$cut.group,
                          alternative="two.sided",
                          var.equal=TRUE)
  T.method <-c(T.method, t.test.result$method)
  T.equality <-c(T.equality,"YES")
  T.statistic <-c(T.statistic,t.test.result$statistic)
  T.pvalue <-c(T.pvalue, t.test.result$p.value)
}else{
  #2단계가 깨질경우
  t.test.result <- t.test(unlist(diamonds[,i])~diamonds$cut.group,
                          alternative="two.sided",
                          var.equal=FALSE)
  
  T.method <-c(T.method, t.test.result$method)
  T.equality <-c(T.equality,"NO")
  T.statistic <-c(T.statistic, t.test.result$statistic)
  T.pvalue <-c(T.pvalue, t.test.result$p.value)
}
}else{
#1단계가 깨졌을 경우
  wilcoxn.test.result <- wilcox.test(unlist(diamonds[,i])~diamonds$cut.group,
                                    alternative="two.sided")
  
  T.method <-c(T.method, wilcoxn.test.result$method)
  T.equality <-c(T.equality,"NULL")
  T.statistic <-c(T.statistic,wilcoxn.test.result$statistic)
  T.pvalue <-c(T.pvalue, wilcoxn.test.result$p.value)
}
  }

#데이터 저장
resultDF <- data.frame(Variable = colnames(diamonds)[c(1,5:10)],
                       Method = T.method,
                       Equality= T.equality,
                       Statistic= T.statistic,
                       PValue= T.pvalue)
View(resultDF)


# 3)Paired Test###########################################################
#동일한 대상자에게 사전/사후 간의 양적 자료에 변화가 있는지를 분석하는 방법
#양적자료 2쌍
#같은 대상의 양적자료인데 사전, 사후여야함 ex) 다이어트 전후

#순서
#1) 정규성
#2) 등분산검정
#3) Paired t-test

#가설1 with SAT
# 귀무가설: 강의 만족도에 변동없음(mu1=mu2)
# 대립가설: 강의 만족도 변동있음 (mu1<mu2)

#1단계: 정규성 검정
#귀무가설: (사전-사후)를 뺸 값은 정규분포 따름
#대립가설: (사전-사후)룰 뺀 값은 정규분포를 따르지 않음 

sat <- SAT

sat$diff <- sat$pre - sat$post
View(sat)
shapiro.test(sat$diff)

# 2단계 Wilcoxon's signed rank test
wilcox.test(sat$pre, sat$post,
            alternative = "less",
            paired= TRUE)

#or
wilcox.test(sat$diff,
            alternative = "less")

install.packages("exactRankTests")
library(exactRankTests)

exactRankTests::wilcox.exact(sat$diff,
                             alternative="less")
#if 정규성 만족?
t.test(sat$pre, sat$post,
       alternative = "less",
       paired = TRUE) # paried=T 아니면 단순 two sample t-test
