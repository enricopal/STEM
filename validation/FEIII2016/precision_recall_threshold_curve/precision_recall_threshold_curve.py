import os
import numpy as np
import pandas as pd
import subprocess
import optparse
from sfem.duke_output_parser import duke_output_parser
from sfem.scorer import scorer_return
from collections import Counter
from sklearn.svm import SVC
from sklearn import cross_validation
from sklearn import grid_search
from sfem.stacking_create_training_set import stacking_create_training_set
import xml.etree.ElementTree as ET

#defining the options of the script

#INPUTS: -i duke_config.xml, -N number_of_configurations, -a amplitude_of_perturbation, -g gold_standard_name

parser = optparse.OptionParser()
parser.add_option('-i','--input', dest = 'file_name', help = 'file_name')
parser.add_option('-g','--gold', dest = 'gold_standard_name', help = 'gold_standard_name')

(options, args) = parser.parse_args()

if options.file_name is None:
   options.file_name = raw_input('Enter file name:')


if options.gold_standard_name is None:
    options.gold_standard_name = raw_input('Enter gold standard file name:')


file_name = options.file_name #define the variables
gold_standard_name = options.gold_standard_name

#open files for writing

gold_standard_read = open(gold_standard_name,'rU')

#iterate for each tweaked configuration

#read actual threshold

tree = ET.parse(file_name)
root = tree.getroot()

for thresh in root.iter('threshold'):
    central_thresh = float(thresh.text) #central value of the threshold

thresholds = np.linspace(0.05, 0.90, 20)

scores = open('precision_recall_curve_scores.txt','w')

scores.write('p,r,f\n')

for threshold in thresholds:

    output_file_raw = open('duke_output_raw_precision_recall_curve.txt','w') #open and clean new file with duke output

    for thresh in root.iter('threshold'):
        thresh.text = str(threshold)
        thresh.set('updated','yes')

    tree.write('../../../config/FEIII2016/copy_T2.xml') 

    java_command = ["java","-Xmx5000m", "-cp", "../../../lib/Duke/duke-core/target/*:../../../lib/Duke/duke-dist/target/*:../../../lib/Duke/duke-es/target/*:../../../lib/Duke/duke-json/target/*:../../../lib/Duke/duke-lucene/target/*:../../../lib/Duke/duke-mapdb/target/*:../../../lib/Duke/duke-mongodb/target/*:../../../lib/Duke/duke-server/target/*:../../../lib/Duke/lucene_jar/*", "no.priv.garshol.duke.Duke", "--showmatches","--batchsize=100000", "--threads=4", "../../../config/FEIII2016/copy_T2.xml"]

    output_file_raw.write(subprocess.check_output(java_command)) #call duke on the copy.xml file and write the raw output on file
 
    output_file_raw.close() #close the file

    duke_output_parser('duke_output_raw_precision_recall_curve.txt', 'duke_output_precision_recall_curve.csv','FFIEC','SEC')
    
    scores.write(str(scorer_return('duke_output_precision_recall_curve.csv',gold_standard_name)).strip('(').strip(')'))
    scores.write('\n')
      
gold_standard_read.close()

scores.close()
