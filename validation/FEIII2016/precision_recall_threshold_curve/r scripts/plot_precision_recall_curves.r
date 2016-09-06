library(ggplot2)
setwd('/home/enrico/Dropbox/STEM/validation/FEIII2016/precision_recall_threshold_curve/')

#this script plots p,r,f as a function of the threshold

data_read <- read.csv('../precision_recall_curve_scores_nostack.csv')
stacking_data_read <- read.csv('stacking_curves/precision_recall_curve_scores_stacking_test_set.csv')

thresholds <- seq(from = 0.01, to = 0.9562069, by = (0.9562069-0.01)/28)


data <- cbind(data_read,thresholds)

ggplot(xlab="Threshold", ylab="") + 
  geom_line(data = data, aes(x = thresholds, y = p, colour="p"),size = 3) +
  geom_point(data = data, aes(x = thresholds, y = p), size=3, shape=21, fill="white") +
  geom_line(data = data, aes(x = thresholds, y = r,colour="r"), size = 3) +
  geom_point(data = data, aes(x = thresholds, y = r),  size=3, shape=21, fill="white") +
  #geom_line(data = data, aes(x = thresholds, y = f,colour="f")) +
  #geom_point(data = data, aes(x = thresholds, y = f),size=2, shape=21, fill="white") +
  ylab("")+
  scale_colour_manual(name="Precision-Recall curves",
                    breaks=c("p", "r"),
                    values=c("green", "red"), 
                    labels=c("Precision", "Recall"))

data_stacking <- cbind(stacking_data_read,thresholds)

ggplot(xlab="Threshold", ylab="") + 
  geom_line(data = data_stacking, aes(x = thresholds, y = p_stack,colour="p_stack")) +
  geom_point(data = data_stacking, aes(x = thresholds, y = p_stack), size=2, shape=21, fill="white") +
  geom_line(data = data_stacking, aes(x = thresholds, y = r_stack,colour="r_stack")) +
  geom_point(data = data_stacking, aes(x = thresholds, y = r_stack),  size=2, shape=21, fill="white") +
  geom_line(data = data_stacking, aes(x = thresholds, y = f_stack,colour="f_stack")) +
  geom_point(data = data_stacking, aes(x = thresholds, y = f_stack),size=2, shape=21, fill="white") +
  ylab("")+
  scale_colour_manual(name="Precision-Recall curves",
                      breaks=c("p_stack", "r_stack", "f_stack"),
                      values=c("green", "red", "blue"), 
                      labels=c("Precision", "Recall", "F-measure"))


#estimating the growth speed with a linear fit
indexes_fit <- indexes/100 #rescale to 0-1
fit <- lm(pointstoplot ~ indexes_fit, weights = 1/sds**2) #setting the estimated variances as errors 
summary(fit)

