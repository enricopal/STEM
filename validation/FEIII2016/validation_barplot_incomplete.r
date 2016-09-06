library(ggplot2)
setwd('/home/enrico/Dropbox/SFEM/validation/FEIII2016/')

data <- read.csv('ml_validation_results_incomplete.csv')

#list of f-score with 0.1 of the gold standard
F1 <- data[data$frac == 0.1,]$F
F2 <- data[data$frac == 0.2,]$F
F3 <- data[data$frac == 0.3,]$F
F4 <- data[data$frac == 0.4,]$F
F5 <- data[data$frac == 0.5,]$F
F6 <- data[data$frac == 0.6,]$F

m1 = mean(F1)
m2 = mean(F2)
m3 = mean(F3)
m4 = mean(F4)
m5 = mean(F5)
m6 = mean(F6)

min1 = min(F1)
min2 = min(F2)
min3 = min(F3)
min4 = min(F4)
min5 = min(F5)
min6 = min(F6)

max1 = max(F1)
max2 = max(F2)
max3 = max(F3)
max4 = max(F4)
max5 = max(F5)
max6 = max(F6)


pointstoplot<-c(m1,m2,m3,m4,m5,m6)

s1 = sd(p1)
s2 = sd(p2)
s3 = sd(p3)
s4 = sd(p4)
s5 = sd(p5)
s6 = sd(p6)

indexes<-c(10,20,30,40,50,60)
sds<-c(s1,s2,s3,s4,s5,s6)
mins<-c(min1,min2,min3,min4,min5,min6)
maxes<-c(max1,max2,max3,max4,max5,max6)
up_bound <- c(m1+s1,m2+s2,m3+s3,m4+s4,m5+s5,m6+s6)
low_bound <- c(m1-s1,m2-s2,m3-s3,m4-s4,m5-s5,m6-s6)
x = cbind(data.frame(indexes,pointstoplot, sds, low_bound, up_bound))

qplot(x=indexes, y=pointstoplot, xlab="Percentage of Training Data Used", ylab="F-Measure") + geom_errorbar(aes(ymin=low_bound, ymax=up_bound))

#estimating the growth speed with a linear fit
indexes_fit <- indexes/100 #rescale to 0-1
fit <- lm(pointstoplot ~ indexes_fit, weights = 1/sds**2) #setting the estimated variances as errors 
summary(fit)

