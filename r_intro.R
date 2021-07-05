#디렉토리 지정
getwd() # print the current working directory - cwd 
setwd("C:/Users/haley/R/1week_R/basic") # change to mydirectory 

#Importing data
d <- read.csv(file='malaria.txt')
d <- read.table(file='malaria.txt',header=T)
View(d)
##Vewing data
head(d, n=10) # print first 10 rows of malaria
tail(d, n=5) # print last 5 rows of malaria
summary(d)
ls() # list objects in the working environment
dim(d)# dimensions of an malaria
names(d) # list the variables in malaria
str(d) # list the structure of malaria
d$v1 <-factor(d$mal) #adding the V1 columm
levels(d$v1) # list levels of factor v1 in malaria
dim(d) # dimensions of an malaria
class(d) # class of an malaria (numeric, matrix, dataframe, etc)
View(d)

#exporting
#To an CSV file
write.csv(d,"C:/Users/haley/R/1week_R/basic/sample.csv")



#####data types#####
##Vectors
a <- c(1,2,5.3,6,-2,4) #numeric vector
str(a)

b <- c("one","two","three") #character vector
str(b)

c <- c(TRUE,TRUE,TRUE,FALSE,TRUE,FALSE) #logical vector

a[2]
a[c(2,4,6)] #2nd and 4th elements of vector

#Factors (범주형)
gender <- c(rep("male",20), rep("female", 30)) #rep() 반복되는 수를 생성하는 함수
gender1 <- factor(gender)
g <- rep(1:3,10)
g1 <- factor(g)

# R now treats gender as a nominal variable 
summary(gender)
summary(gender1)

# generates 5 x 4 numeric matrix
y<-matrix(1:20, nrow=5,ncol=4) #(범위,행,열) 
y[,4] # 4th column of matrix
y[3,] # 3rd row of matrix 
y[2:4,1:3] # rows  2,3,4 of columns 1,2,3 // 행 2에서 4, 열 1에서 3
y[c(2,4),c(1,3)] # row 2,4에 있으면서 col 1,3에 있는 변수

#Dataframes  
num <- c(1,2,3,4)
col <- c("red", "white", "red", NA)
logi <- c(TRUE,TRUE,TRUE,FALSE)
cb1 <- rbind(num,col,logi) #행바인드 cbind// cbind열바인드
cb <- cbind(num,col,logi) #cbind를 이용하는게 더 편리하고 좋음. 
mydata <- data.frame(cb) # same as:mydata <- data.frame(num,col,logi)
names(mydata1) <- c("ID","Color","Passed") # variable names // 이름 지정해줄께 아이디 컬러 패스드,변수명을 지정해주는거야.

is.matrix(y)
is.matrix(mydata) #매트릭스니?
is.data.frame(mydata) #데이터 프레임이니?
class(mydata) 


#Arrays
di <-array(1:30,dim=c(2,5,3)) #디멘젼 2x5 행렬을 세개만든다.
di
class(di)


#Lists // 서로 다른 데이터 형태를 묶은 것.   
# example of a list with 4 components - 
# a string, a numeric vector, a matrix, and a scaler 
w <- list(name="Fred", mynumbers=a, mymatrix=y, age=5.3)
w[[2]][3]




#Value labels
# variable v1 is coded 1, 2 or 3
e1<-c(1,1,1,2,2,3)
# we want to attach value labels 1=red, 2=blue, 3=green
e2 <- factor(e1, levels = c(1,2,3), labels = c("red", "blue", "green")) 
d$v2 <- factor(d$v1,levels=c(0,1), labels=c("Yes","NO"))

#Testing for missing values
y <- c(1,2,3,NA)
mean(y)
is.na(y) # returns a vector (F F F T) 
which(is.na(y))

#Recoding values to missing
d[d$age==99,] #60번쨰 99살인 사람이 
d[60,"age"] <- NA #말라리아 에서 60번째 인사람을 결측값처리한다.
d[60,] #d[,60] 

#Excluding missing values from analyses
x <- c(1,2,NA,3)
mean(x)          # returns NA
mean(x, na.rm=T) # returns 2 


##getting help
help.start() # general help
help(t.test) #? help about function 
? t.test 



##Install packages
install.packages("ggplot2")
install.packages("dplyr")
library(ggplot2)
library(dplyr)

##useful fuctions
# for vector
a=c(-1,-2,3,4,5)

length(a) 	# number of elements or components
length(d$age)
str(a)	# internal strucutre of an object
class(a)  	# class or type of an object

dim(a)

# for matrix
y
length(y)	# number of elements or components
str(y)	# internal strucutre of an object
class(y)	# class or type of an object
dim(y)	# dimension of an object
length(malaria)

#for list
w
length(w)	# number of elements or components
str(w)	# structure of an object 
class(w)	# class or type of an object
attributes(w)	#attribute list
w$name #자료에서 하나를 소환하는거. 
w$mynumbers[1]
w$myarray[1,1,1]
w$age #age는 모양. 
w[[3]][2,3]

#c(object,object,...) 		# combine objects into a vector
#cbind(object, object, ...) # combine objects as columns
#rbind(object, object, ...) # combine objects as rows 


a=c(1, 2.4, 3.2,0.5, 0.7, 0.9, 4)

b <- a+1

a
b

c(a,b)

mycbind=cbind(a,b) # combine objects into a vector
myrbind=rbind(a,b) # combine objects into a vector
mycbind
myrbind
class(a)
class(b)
class(mycbind)
rownames(mycbind)=c("Sun","Mon","Tue","Wed","Thur","Fri","Sat") #행변수이름지정
colnames(mycbind)=c("TV watching","Exercise") #열변수이름지정
mycbind