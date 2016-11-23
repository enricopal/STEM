import numpy as np
import pandas as pd
import optparse
from sklearn.svm import SVC
from sklearn import cross_validation
from sklearn import grid_search
import sklearn.metrics


#PARSE ARGUMENTS

parser = optparse.OptionParser()
parser.add_option('-g','--gold', dest = 'gold_standard_name', help = 'gold_standard_name')
parser.add_option('-t','--train', dest = 'training_set', help='training set name')
parser.add_option('-k','--test', dest = 'test_set', help='test set name')

(options, args) = parser.parse_args()

if options.gold_standard_name is None:
    options.gold_standard_name = raw_input('Enter gold standard file name:')

if options.training_set is None:
    options.training_set = options.gold_standard_name

training_set = options.training_set

gold_standard_name = options.gold_standard_name

test_set = options.test_set

#READ DATA

gs_ml_whole = pd.read_csv(gold_standard_name) #WHOLE GS IN ML FORMAT

train_duke = pd.read_csv(training_set) #TRAINING SET IN DUKE FORMAT

test_duke = pd.read_csv(test_set) #TEST SET IN DUKE FORMAT

#define the IDS to use for testing and select test set in ML format

ids_1_test = test_duke.values[:,1]

ids_2_test = test_duke.values[:,2]

test_ml = gs_ml_whole[(gs_ml_whole.FFIEC_ID.isin(ids_1_test)) & (gs_ml_whole.SEC_ID.isin(ids_2_test))] #those that are in the test data and have the shape of the 1,1,1,0,0,1

#define the IDS to use for train and select training set in ML format

ids_1_train = train_duke.values[:,1]

ids_2_train = train_duke.values[:,2]

train_ml = gs_ml_whole[(gs_ml_whole.FFIEC_ID.isin(ids_1_train)) & (gs_ml_whole.SEC_ID.isin(ids_2_train))]

X_train = train_ml.values[:,2:-1] #x variables

y_train = np.array(train_ml['y']) #class variables

X_test = test_ml.values[:,2:-1] #x variables

y_test = np.array(test_ml['y']) #class variables

#fit an SVM with rbf kernel
clf = SVC( kernel = 'rbf',cache_size = 1000)

parameters = {'gamma' : np.logspace(-9,3,30),'C': np.logspace(-2,10,30)}

gs_rbf = grid_search.GridSearchCV(clf,param_grid=parameters,cv = 4, n_jobs = -1)
gs_rbf.fit(X_train,y_train)

#save the output

gs_rbf = gs_rbf.best_estimator_

output = gs_rbf.predict(X_test)

p = sklearn.metrics.precision_score(y_test,output)

r = sklearn.metrics.recall_score(y_test, output)

f = sklearn.metrics.f1_score(y_test,output)

print "%.3f,%.3f,%.3f" %(p,r,f)