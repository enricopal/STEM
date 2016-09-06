import os
import numpy as np
import pandas as pd
import subprocess
import optparse
from collections import Counter
from sklearn.svm import SVC
from sklearn import cross_validation
from sklearn import grid_search
from stacking_create_training_set import stacking_create_training_set
import xml.etree.ElementTree as ET

#defining the options of the script

#INPUTS: -i duke_config.xml, -N number_of_configurations, -a amplitude_of_perturbation, -g gold_standard_name

parser = optparse.OptionParser()
parser.add_option('-i','--input', dest = 'file_name', help = 'file_name')
parser.add_option('-g','--gold', dest = 'gold_standard_name', help = 'gold_standard_name')

(options, args) = parser.parse_args()

if options.file_name is None:
   options.file_name = raw_input('Enter configuration file path:')


if options.gold_standard_name is None:
    options.gold_standard_name = raw_input('Enter gold standard file path:')


file_name = options.file_name #define the variables
gold_standard_name = options.gold_standard_name

#gold standard path

gold_standard_read = open(gold_standard_name,'rU')

#parse xml config file

tree = ET.parse(file_name)
root = tree.getroot()

#define the central thresholds to try

central_thresholds = np.linspace(0.01, 0.99,30)

#open the scores file
#scores = open('precision_recall_curve_scores_stacking.txt','w')

#write the header of the scores file
#scores.write('p,r,f\n')
os.system('echo p,r,f > precision_recall_curve_scores_stacking.csv')


#iterate over all possible central value of threshold
for central_threshold in central_thresholds:

    print central_threshold
    #modify the central threshold
    for thresh in root.iter('threshold'):
        thresh.text = str(central_threshold)
        thresh.set('updated','yes')

    #write it to a file named copy_T2
    tree.write('../../../config/FEIII2016/copy_central.xml') 
    #call sem on copy_T2
    os.system('python ensemble_duke_T2_stacking_prfoutput_cv.py -i ../../../config/FEIII2016/copy_central.xml -g ../../../data/FEIII2016/gs/FFIEC-SEC-GroundTruth.csv -N 10 -a 0.2 >> precision_recall_curve_scores_stacking_crossval.csv')
    os.system('cat precision_recall_curve_scores_stacking_crossval.csv')

gold_standard_read.close()
    
#scores.close()


