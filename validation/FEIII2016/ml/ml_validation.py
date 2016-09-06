import numpy as np
import pandas as pd
import optparse
from sklearn.svm import SVC
from sklearn import cross_validation
from sklearn import grid_search

parser = optparse.OptionParser()
parser.add_option('-g','--gold', dest = 'gold_standard_name', help = 'gold_standard_name')

(options, args) = parser.parse_args()

if options.gold_standard_name is None:
    options.gold_standard_name = raw_input('Enter gold standard file name:')

gold_standard_name = options.gold_standard_name

data = pd.read_csv(gold_standard_name)

X = data.values[:,2:-1] #x variables, the last one is the y
y = np.array(data['y']) #class variables

#print X,y

#fit an SVM with rbf kernel
clf = SVC( kernel = 'rbf',cache_size = 1000)
#parameters = [{'kernel' : ['rbf'],'gamma' : np.logspace(-9,3,30),'C': np.logspace(-2,10,30)}, {'kernel' : ['linear'], 'C': np.logspace(-2,10,30)}]
parameters = {'gamma' : np.logspace(-9,3,30),'C': np.logspace(-2,10,30)}

gs_rbf = grid_search.GridSearchCV(clf,param_grid=parameters,cv = 4)
gs_rbf.fit(X,y)

#print the results

#compute the cross validation score
clf = gs_rbf.best_estimator_

precision_cross_scores = cross_validation.cross_val_score(clf, X, y, cv = 4, scoring = 'precision')
recall_cross_scores = cross_validation.cross_val_score(clf, X, y, cv = 4, scoring = 'recall')
f1_cross_scores = cross_validation.cross_val_score(clf, X, y, cv = 4, scoring = 'f1')

print "%.3f,%.3f,%.3f" %(np.mean(precision_cross_scores),np.mean(recall_cross_scores),np.mean(f1_cross_scores))