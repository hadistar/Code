#Pacakege list 
getwd()
setwd("C:/Users/haley/Desktop")
library(ggplot2)
library(dplyr)
library(Rmisc)
library(readxl)


d <- read_excel("C:/Users/haley/Desktop/risk_assessment_210406.xlsx")
d <- d %>% filter(season != "anuual")
d <- d[,c(9:16)] #농도만 
View(d) 
dim(d)

#변수 선언
################################################################################
{Ring_f <- 30;Ring_m <- 30
EF_f <- 180;EF_m <- 180
ED_f <- 6;ED_m <- 24
BW_f <- 15;BW_m <- 70
SA_f <- 2800;SA_m <- 57002
AF_f <- 0.2;AF_m <- 0.07
ABS_f <- 0.001;ABS_m <- 0.001
AT1_f <- 365*ED_c;AT1_m <- 365*ED_m; #Inhaltation/ HQ
AT1_f_c <- 365*70;AT1_m_c <- 365*70; #dermal&ing/ ILCR
AT2_f <- 365*ED_c*24;AT2_m <- 365*ED_m*24; #Inhaltation/ HQ
AT2_f_c <- 365*70*24;AT2_m_c <- 365*70*24; #Inhaltation/ ILCR
ET_f <- 6;ET_m<-6
CF <-10^-3}

{RfCi_V <- 1.00E-04; RfCi_Cr <- 2.86E-05; RfCi_Mn <- 5.00E-05;RfCi_Ni <- 1.40E-05; 
RfCi_Cu <- 0.0402;RfCi_Zn <- 3.01E-01; RfCi_As <- 1.50E-05
IUR_Cr <- 8.40E-02;IUR_Ni <- 2.40E-04;IUR_Pb <- 8.00E-05;IUR_As <- 4.30E-03}

{RfDo_V <- 5.00E-03; RfDo_Cr <- 3.00E-04; RfDo_Mn <- 2.40E-02;RfDo_Ni <- 1.10E-02;
  RfDo_Cu <- 0.04;RfDo_Zn <- 3.00E-01; RfDo_As <- 3.00E-04
SFo_Cr <- 5.00E-01;SFo_Ni <- 1.70E+00;SFo_Pb <- 8.50E-03;SFo_As <- 1.50E+00}
################################################################################
#ADD_ILCR
################################################################################
#흡입노출 ADD_ILCR
{{ADDinh_f_ILCR <- (d*ET_f*EF_f*ED_f)/613200
ADDinh_m_ILCR <- (d*ET_m*EF_m*ED_m)/613200}

#피부노출 ADD_ILCR
{ADDderm_f_ILCR <- d*((SA_f*AF_f*ABS_f*EF_f*ED_f)*CF/(BW_f*AT1_f_c))
  ADDderm_m_ILCR <- d*((SA_m*AF_m*ABS_m*EF_m*ED_m)*CF/(BW_m*AT1_m_c))}

#섭취노출 ADD_ILCR
{ADDing_f_ILCR <- d*((Ring_f*EF_f*ED_f)*CF/(BW_f*AT1_f_f))
  ADDing_m_ILCR <- d*((Ring_m*EF_m*ED_m)*CF/(BW_m*AT1_m_c))}}
################################################################################

#ADD_HQ
################################################################################
#흡입노출 ADD_HQ
{{ADDinh_f <- d*((ET_f*EF_f*ED_f)/613200)
ADDinh_m <- d*((ET_m*EF_m*ED_m)/613200)}

#피부노출 ADD_HQ
{ADDderm_f <- d*((SA_f*AF_f*ABS_f*EF_f*ED_f)*CF/(BW_f*AT1_f))
ADDderm_m <- d*((SA_m*AF_m*ABS_m*EF_m*ED_m)*CF/(BW_m*AT1_m))}

#섭취노출 ADD_HQ
{ADDing_f <- d*((Ring_f*EF_f*ED_f)*CF/(BW_f*AT1_f))
 ADDing_m <- d*((Ring_m*EF_m*ED_m)*CF/(BW_m*AT1_m))}}
################################################################################


#HQ 여성
################################################################################
{HQ_V_f <- (ADDinh_f$V/(RfCi_V*1000))+(ADDderm_f$V/(RfDo_V*1))+(ADDing_f$V/RfDo_V)
HQ_Cr_f <- (ADDinh_f$Cr/(RfCi_Cr*1000))+(ADDderm_f$Cr/(RfDo_Cr*1))+(ADDing_f$Cr/RfDo_Cr)
HQ_Mn_f <- (ADDinh_f$Mn/(RfCi_Mn*1000))+(ADDderm_f$Mn/(RfDo_Mn*1))+(ADDing_f$Mn/RfDo_Mn)
HQ_Ni_f <- (ADDinh_f$Ni/(RfCi_Ni*1000))+(ADDderm_f$Ni/(RfDo_Ni*1))+(ADDing_f$Ni/RfDo_Ni)
HQ_Cu_f <- (ADDinh_f$Cu/(RfCi_Cu*1000))+(ADDderm_f$Cu/(RfDo_Cu*1))+(ADDing_f$Cu/RfDo_Cu)
HQ_Zn_f <- (ADDinh_f$Zn/(RfCi_Zn*1000))+(ADDderm_f$Zn/(RfDo_Zn*1))+(ADDing_f$Zn/RfDo_Zn)
HQ_As_f <- (ADDinh_f$As/(RfCi_As*1000))+(ADDderm_f$As/(RfDo_As*1))+(ADDing_f$As/RfDo_As)}

CI(HQ_V_f, ci=0.95)
CI(HQ_Cr_f, ci=0.95)
CI(HQ_Mn_f, ci=0.95)
CI(HQ_Ni_f, ci=0.95)
CI(HQ_Cu_f, ci=0.95)
CI(HQ_Zn_f, ci=0.95)
CI(HQ_As_f, ci=0.95)

HI_f <- HQ_V_f +HQ_Cr_f + HQ_Mn_f +HQ_Ni_f + HQ_Cu_f + HQ_Zn_f + HQ_As_f 
CI(HI_f, ci=0.95)
################################################################################

#HQ 남성
################################################################################
{HQ_V_m <- (ADDinh_m$V/(RfCi_V*1000))+(ADDderm_m$V/(RfDo_V*1))+(ADDing_m$V/RfDo_V)
HQ_Cr_m <- (ADDinh_m$Cr/(RfCi_Cr*1000))+(ADDderm_m$Cr/(RfDo_Cr*1))+(ADDing_m$Cr/RfDo_Cr)
HQ_Mn_m <- (ADDinh_m$Mn/(RfCi_Mn*1000))+(ADDderm_m$Mn/(RfDo_Mn*1))+(ADDing_m$Mn/RfDo_Mn)
HQ_Ni_m <- (ADDinh_a$Ni/(RfCi_Ni*1000))+(ADDderm_m$Ni/(RfDo_Ni*1))+(ADDing_m$Ni/RfDo_Ni)
HQ_Cu_m <- (ADDinh_a$Cu/(RfCi_Cu*1000))+(ADDderm_m$Cu/(RfDo_Cu*1))+(ADDing_m$Cu/RfDo_Cu)
HQ_Zn_m <- (ADDinh_m$Zn/(RfCi_Zn*1000))+(ADDderm_m$Zn/(RfDo_Zn*1))+(ADDing_m$Zn/RfDo_Zn)
HQ_As_m <- (ADDinh_m$As/(RfCi_As*1000))+(ADDderm_m$As/(RfDo_As*1))+(ADDing_m$As/RfDo_As)}

CI(HQ_V_m, ci=0.95)
CI(HQ_Cr_m, ci=0.95)
CI(HQ_Mn_m, ci=0.95)
CI(HQ_Ni_m, ci=0.95)
CI(HQ_Cu_m, ci=0.95)
CI(HQ_Zn_m, ci=0.95)
CI(HQ_As_m, ci=0.95)

HI_m <- HQ_V_m +HQ_Cr_m + HQ_Mn_m +HQ_Ni_m + HQ_Cu_m + HQ_Zn_m + HQ_As_m 
CI(HI_m, ci=0.95)
################################################################################

#ILCR 여성
################################################################################
{ILCR_Cr_f <- (ADDinh_f_ILCR$Cr*IUR_Cr)+(ADDderm_f_ILCR$Cr*SFo_Cr)+(ADDingf_ILCR$Cr*SFo_Cr)
ILCR_Ni_f <- (ADDinh_f_ILCR$Ni*IUR_Ni)+(ADDderm_f_ILCR$Ni*SFo_Ni)+(ADDing_f_ILCR$Ni*SFo_Ni)
ILCR_Pb_f <- (ADDinh_f_ILCR$Pb*IUR_Pb)+(ADDderm_f_ILCR$Pb*SFo_Pb)+(ADDing_f_ILCR$Cr*SFo_Pb)
ILCR_As_f <- (ADDinh_f_ILCR$As*IUR_As)+(ADDderm_f_ILCR$As*SFo_As)+(ADDing_f_ILCR$As*SFo_As)}

CI(ILCR_Cr_f, ci=0.95)
CI(ILCR_Ni_f, ci=0.95)
CI(ILCR_Pb_f, ci=0.95)
CI(ILCR_As_f, ci=0.95)
################################################################################

##ILCR 남성
################################################################################
{ILCR_Cr_m <- (ADDinh_m_ILCR$Cr*IUR_Cr)+(ADDderm_m_ILCR$Cr*SFo_Cr)+(ADDing_m_ILCR$Cr*SFo_Cr)
ILCR_Ni_m <- (ADDinh_m_ILCR$Ni*IUR_Ni)+(ADDderm_m_ILCR$Ni*SFo_Ni)+(ADDing_m_ILCR$Ni*SFo_Ni)
ILCR_Pb_m <- (ADDinh_m_ILCR$Pb*IUR_Pb)+(ADDderm_m_ILCR$Pb*SFo_Pb)+(ADDing_m_ILCR$Cr*SFo_Pb)
ILCR_As_m <- (ADDinh_m_ILCR$As*IUR_As)+(ADDderm_m_ILCR$As*SFo_As)+(ADDing_m_ILCR$As*SFo_As)}

CI(ILCR_Cr_m, ci=0.95)
CI(ILCR_Ni_m, ci=0.95)
CI(ILCR_Pb_m, ci=0.95)
CI(ILCR_As_m, ci=0.95)

################################################################################

#ILCR_Inha_female
CI((ADDinh_f_ILCR$Cr*IUR_Cr),ci=0.95)
CI((ADDinh_f_ILCR$Ni*IUR_Ni),ci=0.95)
CI((ADDinh_f_ILCR$Pb*IUR_Pb),ci=0.95)
CI((ADDinh_f_ILCR$As*IUR_As),ci=0.95)

#ILCR_Inha_male
CI((ADDinh_m_ILCR$Cr*IUR_Cr),ci=0.95)
CI((ADDinh_m_ILCR$Ni*IUR_Ni),ci=0.95)
CI((ADDinh_m_ILCR$Pb*IUR_Pb),ci=0.95)
CI((ADDinh_m_ILCR$As*IUR_As),ci=0.95)

#ILCR_derm_female
CI((ADDderm_f_ILCR$Cr*SFo_Cr),ci=0.95)
CI((ADDderm_f_ILCR$Ni*SFo_Ni),ci=0.95)
CI((ADDderm_f_ILCR$Pb*SFo_Pb),ci=0.95)
CI((ADDderm_f_ILCR$As*SFo_As),ci=0.95)

#ILCR_derm_male
CI((ADDderm_m_ILCR$Cr*SFo_Cr),ci=0.95)
CI((ADDderm_m_ILCR$Ni*SFo_Ni),ci=0.95)
CI((ADDderm_m_ILCR$Pb*SFo_Pb),ci=0.95)
CI((ADDderm_m_ILCR$As*SFo_As),ci=0.95)

##ILCR_ing_female
CI((ADDing_f_ILCR$Cr*SFo_Cr),ci=0.95)
CI((ADDing_f_ILCR$Ni*SFo_Ni),ci=0.95)
CI((ADDing_f_ILCR$Pb*SFo_Pb),ci=0.95)
CI((ADDing_f_ILCR$As*SFo_As),ci=0.95)

CI((ADDing_f_ILCR$Cr*SFo_Cr),ci=0.95)
CI((ADDing_f_ILCR$Ni*SFo_Ni),ci=0.95)
CI((ADDing_f_ILCR$Pb*SFo_Pb),ci=0.95)
CI((ADDing_f_ILCR$As*SFo_As),ci=0.95)

#HQ_female_Inhalation
CI((ADDinh_f$V/(RfCi_V*1000)),ci=0.95)
CI((ADDinh_f$Cr/(RfCi_Cr*1000)),ci=0.95)
CI((ADDinh_f$Mn/(RfCi_Mn*1000)),ci=0.95)
CI((ADDinh_f$Ni/(RfCi_Ni*1000)),ci=0.95)
CI((ADDinh_f$Cu/(RfCi_Cu*1000)),ci=0.95)
CI((ADDinh_f$Zn/(RfCi_Zn*1000)),ci=0.95)
CI((ADDinh_f$As/(RfCi_As*1000)),ci=0.95)

#HQ_male_Inhalation
CI((ADDinh_m$V/(RfCi_V*1000)),ci=0.95)
CI((ADDinh_m$Cr/(RfCi_Cr*1000)),ci=0.95)
CI((ADDinh_m$Mn/(RfCi_Mn*1000)),ci=0.95)
CI((ADDinh_m$Ni/(RfCi_Ni*1000)),ci=0.95)
CI((ADDinh_m$Cu/(RfCi_Cu*1000)),ci=0.95)
CI((ADDinh_m$Zn/(RfCi_Zn*1000)),ci=0.95)
CI((ADDinh_m$As/(RfCi_As*1000)),ci=0.95)

#HQ_female_dermal
CI(((ADDderm_f$V/(RfDo_V*1))),ci=0.95)
CI(((ADDderm_f$Cr/(RfDo_Cr*1))),ci=0.95)
CI(((ADDderm_f$Mn/(RfDo_Mn*1))),ci=0.95)
CI(((ADDderm_f$Ni/(RfDo_Ni*1))),ci=0.95)
CI(((ADDderm_f$Cu/(RfDo_Cu*1))),ci=0.95)
CI(((ADDderm_f$Zn/(RfDo_Zn*1))),ci=0.95)
CI(((ADDderm_f$As/(RfDo_As*1))),ci=0.95)

#HQ_male_dermal
CI(((ADDderm_m$V/(RfDo_V*1))),ci=0.95)
CI(((ADDderm_m$Cr/(RfDo_Cr*1))),ci=0.95)
CI(((ADDderm_m$Mn/(RfDo_Mn*1))),ci=0.95)
CI(((ADDderm_m$Ni/(RfDo_Ni*1))),ci=0.95)
CI(((ADDderm_m$Cu/(RfDo_Cu*1))),ci=0.95)
CI(((ADDderm_m$Zn/(RfDo_Zn*1))),ci=0.95)
CI(((ADDderm_m$As/(RfDo_As*1))),ci=0.95)

#HQ_female_ing
CI((ADDing_f$V/RfDo_V),ci=0.95)
CI((ADDing_f$Cr/RfDo_Cr),ci=0.95)
CI((ADDing_f$Mn/RfDo_Mn),ci=0.95)
CI((ADDing_f$Ni/RfDo_Ni),ci=0.95)
CI((ADDing_f$Cu/RfDo_Cu),ci=0.95)
CI((ADDing_f$Zn/RfDo_Zn),ci=0.95)
CI((ADDing_f$As/RfDo_As),ci=0.95)

#HQ_male_ing
CI((ADDing_m$V/RfDo_V),ci=0.95)
CI((ADDing_m$Cr/RfDo_Cr),ci=0.95)
CI((ADDing_m$Mn/RfDo_Mn),ci=0.95)
CI((ADDing_m$Ni/RfDo_Ni),ci=0.95)
CI((ADDing_m$Cu/RfDo_Cu),ci=0.95)
CI((ADDing_m$Zn/RfDo_Zn),ci=0.95)
CI((ADDing_m$As/RfDo_As),ci=0.95)
