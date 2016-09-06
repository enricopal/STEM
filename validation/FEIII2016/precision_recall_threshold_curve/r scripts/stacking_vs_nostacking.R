library(ggplot2)
setwd('/home/enrico/Dropbox/STEM/validation/FEIII2016/precision_recall_threshold_curve/')

stacking_data <- read.csv('stacking_curves/precision_recall_curve_scores_stacking_cross_val.csv')
nostacking_data <- read.csv('precision_recall_curve_nostack.csv')

thresholds <- seq(from = 0.05, to = 0.90, by = (0.90-0.05)/19)

data <- cbind(stacking_data[2:19,],nostacking_data[2:19,],thresholds[2:19])

ggplot(xlab="Threshold", ylab="") + 
  geom_line(data = data, aes(x = thresholds, y = p_cv,colour="p_cv")) +
  geom_point(data = data, aes(x = thresholds, y = p_cv), size=2, shape=21, fill="white") +
  #geom_line(data = data, aes(x = thresholds, y = r_cv,colour="r_cv")) +
  #geom_point(data = data, aes(x = thresholds, y = r_cv),  size=2, shape=21, fill="white") +
  #geom_line(data = data, aes(x = thresholds[2:19], y = p_stack, colour="r_stack")) +
  #geom_point(data = data, aes(x = thresholds[2:19], y = p_stack),size=2, shape=21, fill="white") +
  #geom_line(data = data, aes(x = thresholds, y = p,colour="p")) +
  #geom_point(data = data, aes(x = thresholds, y = p), size=2, shape=21, fill="white") +
  #geom_line(data = data, aes(x = thresholds, y = r,colour="r")) +
  #geom_point(data = data, aes(x = thresholds, y = r),  size=2, shape=21, fill="white") +
  #geom_line(data = data, aes(x = thresholds[2:19], y = p,colour="r")) +
  #geom_point(data = data, aes(x = thresholds[2:19], y = p),size=2, shape=21, fill="white") +
  ylab("")+
  xlab("threshold")+
  scale_colour_manual(name="Precision",
                      breaks=c("r_stack", "r"),
                      values=c("green", "blue"), 
                      labels=c("p-stacking","-no_stacking"))


library(Rmisc)

p_plot <- ggplot(xlab="Threshold", ylab="") + 
  geom_line(data = data, aes(x = thresholds[2:19], y = p_cv, colour="r_stack")) +
  geom_point(data = data, aes(x = thresholds[2:19], y = p_cv),size=2, shape=21, fill="white") +
  geom_line(data = data, aes(x = thresholds[2:19], y = p,colour="r")) +
  geom_point(data = data, aes(x = thresholds[2:19], y = p),size=2, shape=21, fill="white") +
  ylab("")+
  xlab("threshold")+
  scale_colour_manual(name="Precision",
                      breaks=c("r_stack", "r"),
                      values=c("green", "blue"), 
                      labels=c("p-stacking","p-no_stacking"))

r_plot <- ggplot(xlab="Threshold", ylab="") + 
  geom_line(data = data, aes(x = thresholds[2:19], y = r_cv, colour="r_stack")) +
  geom_point(data = data, aes(x = thresholds[2:19], y = r_cv),size=2, shape=21, fill="white") +
  geom_line(data = data, aes(x = thresholds[2:19], y = r,colour="r")) +
  geom_point(data = data, aes(x = thresholds[2:19], y = r),size=2, shape=21, fill="white") +
  ylab("")+
  xlab("threshold")+
  scale_colour_manual(name="Recall",
                      breaks=c("r_stack", "r"),
                      values=c("green", "blue"), 
                      labels=c("r-stacking","r-no_stacking"))

f_plot <- ggplot(xlab="Threshold", ylab="") + 
  geom_line(data = data, aes(x = thresholds[2:19], y = f_cv, colour="r_stack")) +
  geom_point(data = data, aes(x = thresholds[2:19], y = f_cv),size=2, shape=21, fill="white") +
  geom_line(data = data, aes(x = thresholds[2:19], y = f,colour="r")) +
  geom_point(data = data, aes(x = thresholds[2:19], y = f),size=2, shape=21, fill="white") +
  ylab("")+
  xlab("threshold")+
  scale_colour_manual(name="F-score",
                      breaks=c("r_stack", "r"),
                      values=c("green", "blue"), 
                      labels=c("f-stacking","f-no_stacking"))

multiplot(p_plot,r_plot,f_plot)
  