import os
import numpy as np
import pandas as pd
import subprocess
import optparse
from sklearn.svm import SVC
from sklearn import cross_validation
from sklearn import grid_search
from stacking_create_training_set_silk import stacking_create_training_set_silk
import xml.etree.ElementTree as ET
import time

#defining the options of the script

#INPUTS: -i silk_config.xml, -N number_of_configurations, -a amplitude_of_perturbation, -g gold_standard_name

start_time = time.time()

parser = optparse.OptionParser()
parser.add_option('-i','--input', dest = 'file_name', help = 'file_name')
parser.add_option('-N','--number', dest = 'N', help = 'number of classifiers',type = int)
parser.add_option('-a','--amplitude', dest = 'a', help = 'amplitude of perturbation',type = float)
parser.add_option('-g','--gold', dest = 'gold_standard_name', help = 'gold_standard_name')

(options, args) = parser.parse_args()

if options.file_name is None:
   options.file_name = raw_input('Enter file name:')

if options.N is None:
    options.N = raw_input('Enter number of classifiers:')

if options.a is None:
    options.a = 0.05 #default to 0.05

if options.gold_standard_name is None:
    options.gold_standard_name = raw_input('Enter gold standard file name:')


file_name = options.file_name #define the variables
gold_standard_name = options.gold_standard_name
N = int(options.N)
a = float(options.a)

#open files for writing

output_file_raw = open('ensemble_silk_output_raw_n%d.txt' %N,'w') 

#output_file = open('ensemble_duke_stacking_output_T2_n%d.txt' %N,'w') 

gold_standard_read = open(gold_standard_name,'rU')

#iterate for each tweaked configuration

#read actual threshold

tree = ET.parse(file_name)
root = tree.getroot()

for thresh in root.iter('Output'):
    central_thresh = float(thresh.attrib['minConfidence']) #central value of the threshold
    
for k in root.iter('Output'):
     for b in k.iter('Param'):
             if b.attrib['name'] == 'file':
                     output_file_name =  b.attrib['value']

thresholds = np.linspace(central_thresh - a/2, central_thresh + a/2, N)


for threshold in thresholds:

    for thresh in root.iter('Output'):
        thresh.attrib['minConfidence'] = str(threshold)
        #print thresh.attrib['minConfidence']
     
    tree.write('../config/FEIII2016/copy_ffiec_sec.xml') #write the modified xml to file

    java_command = "java -Xmx5000m -DconfigFile=../config/FEIII2016/copy_ffiec_sec.xml -Dthreads=4 -jar ../lib/Silk/silk.jar"
    
    os.system(java_command)

    data_path = '../config/FEIII2016/'

    #print output_file_name


    silk_output_name = data_path+output_file_name #'FFIEC_LEI.nt'

    #open output file

    silk_output = open(silk_output_name,'rU')

    for i in silk_output.readlines():
        output_file_raw.write(i)

    silk_output.close()

    output_file_raw.write('End of run\n') 

    print "End of run\n"
    
output_file_raw.close()

#create the training set, named training_set_T1_n%d.csv

stacking_create_training_set_silk('ensemble_silk_output_raw_n%d.txt' %N,'training_set_silk_n%d.csv' %N, gold_standard_name, N)

#read it and make machine learning on it

data = pd.read_csv('training_set_silk_n%d.csv' %N)

X = data.values[:,2:(N+2)] #x variables
y = np.array(data['y']) #class variables

#fit an SVM with rbf kernel
clf = SVC( kernel = 'rbf',cache_size = 1000)
#parameters = [{'kernel' : ['rbf'],'gamma' : np.logspace(-9,3,30),'C': np.logspace(-2,10,30)}, {'kernel' : ['linear'], 'C': np.logspace(-2,10,30)}]
parameters = {'gamma' : np.logspace(-9,3,30),'C': np.logspace(-2,10,30)}

gs_rbf = grid_search.GridSearchCV(clf,param_grid=parameters,cv = 4)
gs_rbf.fit(X,y)
#save the output
output = np.reshape(gs_rbf.predict(X),(len(data),1))

#dump it to file

id1_id2_output = np.concatenate((data.values[:,0:2],output), axis = 1)
f = open('results_stacking_silk_n%d.csv' %N, 'w')
for i in id1_id2_output:
    if i[2] == 1: #only reports TP
        f.write(str(i[0]))
        f.write(',')
        f.write(str(i[1]))
        f.write('\n')
        
f.close()


#print "The stacking scoring on the whole set is:\n"
#scorer('results_stacking_silk_n%d.csv'%N,gold_standard_name)

#compute the cross validation score
clf = gs_rbf.best_estimator_

precision_cross_scores = cross_validation.cross_val_score(clf, X, y, cv = 4, scoring = 'precision')
recall_cross_scores = cross_validation.cross_val_score(clf, X, y, cv = 4, scoring = 'recall')
f1_cross_scores = cross_validation.cross_val_score(clf, X, y, cv = 4, scoring = 'f1')

print "The cross validation scores are:\n"
print "Precision: ", np.mean(precision_cross_scores),'\n'
print "Recall: ", np.mean(recall_cross_scores),'\n'
print "F1: ", np.mean(f1_cross_scores),'\n'

print "The best hyper-parameters are:\n"
print gs_rbf.best_params_

#print "The generated thresholds are:\n"
#print thresholds

print("--- %s seconds ---" % (time.time() - start_time))


#print "%.3f,%.3f,%.3f" %(np.mean(precision_cross_scores),np.mean(recall_cross_scores),np.mean(f1_cross_scores))