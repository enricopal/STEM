cross_val_scores <- read.csv('stacking_curves/precision_recall_curve_scores_stacking_cross_val.csv')
test_scores <- read.csv('stacking_curves/precision_recall_curve_scores_stacking_test_set.csv')
thresholds <- seq(from = 0.05, to = 0.90, by = (0.90-0.05)/19)

data <- cbind(cross_val_scores,test_scores,thresholds)

ggplot(xlab="Threshold", ylab="") + 
  #geom_line(data = data, aes(x = thresholds, y = p_cv,colour="p_cv")) +
  #geom_point(data = data, aes(x = thresholds, y = p_cv), size=2, shape=21, fill="white") +
  #geom_line(data = data, aes(x = thresholds, y = r_cv,colour="r_cv")) +
  #geom_point(data = data, aes(x = thresholds, y = r_cv),  size=2, shape=21, fill="white") +
  geom_line(data = data, aes(x = thresholds, y = f_cv,colour="f_cv")) +
  geom_point(data = data, aes(x = thresholds, y = f_cv),size=2, shape=21, fill="white") +
  #geom_line(data = data, aes(x = thresholds, y = p,colour="p")) +
  #geom_point(data = data, aes(x = thresholds, y = p), size=2, shape=21, fill="white") +
  #geom_line(data = data, aes(x = thresholds, y = r,colour="r")) +
  #geom_point(data = data, aes(x = thresholds, y = r),  size=2, shape=21, fill="white") +
  geom_line(data = data, aes(x = thresholds, y = f,colour="f")) +
  geom_point(data = data, aes(x = thresholds, y = f),size=2, shape=21, fill="white") +
  ylab("")+
  scale_colour_manual(name="Precision-Recall curves",
                      breaks=c("f_cv", "f"),
                      values=c("green", "blue"), 
                      labels=c("F-measure_cv","F-measure"))