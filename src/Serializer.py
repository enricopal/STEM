import os
import numpy as np
import pandas as pd
import subprocess
import optparse
from collections import Counter
from sklearn.svm import SVC
from sklearn import cross_validation
from sklearn import grid_search
import stacking_create_training_set
from sklearn.externals import joblib
import xml.etree.ElementTree as ET
import time

#train the STEM model and creates a pickle object that can be loaded successively


class Serializer:

    def __init__(self, file_name, gold_standard_name, N, a):
        self.file_name = file_name
        self.gold_standard_name = gold_standard_name
        self.N = N
        self.a = a


    def serialize_stem_duke(self):

        start_time = time.time()

        print 'Starting the entity matching process'

        file_name = self.file_name #define the variables
        gold_standard_name = self.gold_standard_name
        N = int(self.N)
        a = float(self.a)

        #open files for writing

        path_to_file = gold_standard_name

        path_to_file = path_to_file.split('/gs/')

        path_to_file = path_to_file[0]+'/'

        output_file_raw = open(path_to_file+'ensemble_duke_output_raw_n%d.txt' %N,'w') 

        path_to_config_file = file_name.split('/')
        path_to_config_list = path_to_config_file[0:-1] #the last element is the name of the file, I just want the path
    
        #turn the list into a string by iterating and summing

        path_to_config = ''

        for i in path_to_config_list:
            path_to_config += i 
            path_to_config += '/'

        #output_file = open('ensemble_duke_stacking_output_T2_n%d.txt' %N,'w') 

        gold_standard_read = open(gold_standard_name,'rU')

        #iterate for each tweaked configuration

        #read actual threshold

        tree = ET.parse(file_name)
        root = tree.getroot()

        for thresh in root.iter('threshold'):
            central_thresh = float(thresh.text) #central value of the threshold

        thresholds = np.linspace(central_thresh - a/2, central_thresh + a/2, N)


        for threshold in thresholds:

            for thresh in root.iter('threshold'):
                thresh.text = str(threshold)
                thresh.set('updated','yes')

            path_to_config_and_name = path_to_config+'duke.xml' 

            tree.write(path_to_config_and_name) #generate a new modified configuration file

            java_command = ["java","-Xmx5000m", "-cp", "../lib/Duke/duke-core/target/*:../lib/Duke/duke-dist/target/*:../lib/Duke/duke-es/target/*:../lib/Duke/duke-json/target/*:../lib/Duke/duke-lucene/target/*:../lib/Duke/duke-mapdb/target/*:../lib/Duke/duke-mongodb/target/*:../lib/Duke/duke-server/target/*:../lib/Duke/lucene_jar/*", "no.priv.garshol.duke.Duke", "--showmatches","--batchsize=100000", "--threads=4", "%s" %path_to_config_and_name]

            output_file_raw.write(subprocess.check_output(java_command)) #call duke on the copy.xml file and write the raw output on file
            
            output_file_raw.write('\n')
            output_file_raw.write('End of run\n') 

            print 'End of run\n'

            os.system('rm %s' %path_to_config_and_name) #remove the new modified configuration file
            
        output_file_raw.close()

        #create the training set, named training_set_T1_n%d.csv

        crt_training = stacking_create_training_set.stacking_create_training_set(path_to_file+'ensemble_duke_output_raw_n%d.txt' %N,path_to_file+'training_set_n%d.csv' %N, N)
        crt_training.stacking_create_training_set_duke(gold_standard_name)

        #stacking_create_training_set(path_to_file+'ensemble_duke_output_raw_n%d.txt' %N,path_to_file+'training_set_n%d.csv' %N, gold_standard_name, N)

        #read it and make machine learning on it

        data = pd.read_csv(path_to_file+'training_set_n%d.csv' %N)

        X = data.values[:,2:(N+2)] #x variables
        y = np.array(data['y']) #class variables

        #fit an SVM with rbf kernel
        clf = SVC( kernel = 'rbf',cache_size = 1000)
        #parameters = [{'kernel' : ['rbf'],'gamma' : np.logspace(-9,3,30),'C': np.logspace(-2,10,30)}, {'kernel' : ['linear'], 'C': np.logspace(-2,10,30)}]
        parameters = {'gamma' : np.logspace(-9,3,30),'C': np.logspace(-2,10,30)}

        gs_rbf = grid_search.GridSearchCV(clf,param_grid=parameters,cv = 4)
        gs_rbf.fit(X,y)

        clf = gs_rbf.best_estimator_

        project_name = path_to_config_list[-1]

        joblib.dump(clf, '../models/%s/svm_model_duke_N%d_a%.1f.pkl' %(project_name,N,a))

        print("--- %s seconds ---" % (time.time() - start_time))


    def serialize_stem_silk(self):

        start_time = time.time()

        file_name = self.file_name #define the variables
        gold_standard_name = self.gold_standard_name
        N = int(self.N)
        a = float(self.a)

        path_to_file = gold_standard_name #data/your_experiment/gs/gs.csv

        path_to_file = path_to_file.split('/gs/')

        path_to_file = path_to_file[0]+'/' #data/your_experiment/
        

        path_to_config_file = file_name.split('/')
        path_to_config_list = path_to_config_file[0:-1] #the last element is the name of the file, I just want the path, config/your_experiment/config.xml
    
        #turn the list into a string by iterating and summing

        path_to_config = ''

        for i in path_to_config_list:
            path_to_config += i 
            path_to_config += '/'

        #open files for writing

        output_file_raw = open(path_to_file+'ensemble_silk_output_raw_n%d.txt' %N,'w') 


        #output_file = open('ensemble_duke_stacking_output_T2_n%d.txt' %N,'w') 

        gold_standard_read = open(gold_standard_name,'rU')

        #iterate for each tweaked configuration

        #read actual threshold

        tree = ET.parse(file_name)
        root = tree.getroot()

        for thresh in root.iter('Output'):
            central_thresh = float(thresh.attrib['minConfidence']) #central value of the threshold

        #parsing the silk xml config file to find the name of the output file
 
        for k in root.iter('Output'):
             for b in k.iter('Param'):
                     if b.attrib['name'] == 'file':
                             output_file_name =  b.attrib['value']


        thresholds = np.linspace(central_thresh - a/2, central_thresh + a/2, N) #list of thresholds


        for threshold in thresholds:

            for thresh in root.iter('Output'):
                thresh.attrib['minConfidence'] = str(threshold)
                print thresh.attrib['minConfidence']

            path_to_config_and_name = path_to_config+'silk.xml' #dconfig/your_experiment/silk.xml
             
            tree.write(path_to_config_and_name) #write the modified xml to file

            java_command = "java -Xmx5000m -DconfigFile=%s -Dthreads=4 -jar ../lib/Silk/silk.jar" %path_to_config_and_name
            
            os.system(java_command)

            silk_output_name = path_to_config+output_file_name #config/your_experiment/links.nt

            #open output file

            silk_output = open(silk_output_name,'rU')

            for i in silk_output.readlines():
                output_file_raw.write(i)

            silk_output.close()

            output_file_raw.write('End of run\n') 

            print "End of run\n"

            os.system('rm %s' %path_to_config_and_name) #remove the new modified configuration file

            
        output_file_raw.close()

        #create the training set, named training_set_T1_n%d.csv

        crt_training = stacking_create_training_set.stacking_create_training_set(path_to_file+'ensemble_silk_output_raw_n%d.txt' %N,path_to_file+'training_set_silk_n%d.csv' %N, N)
        crt_training.stacking_create_training_set_silk(gold_standard_name)

        #read it and make machine learning on it

        data = pd.read_csv(path_to_file+'training_set_silk_n%d.csv' %N)

        X = data.values[:,2:(N+2)] #x variables
        y = np.array(data['y']) #class variables

        #fit an SVM with rbf kernel
        clf = SVC( kernel = 'rbf',cache_size = 1000)

        parameters = {'gamma' : np.logspace(-9,3,30),'C': np.logspace(-2,10,30)}

        gs_rbf = grid_search.GridSearchCV(clf,param_grid=parameters,cv = 4)
        gs_rbf.fit(X,y)

        clf = gs_rbf.best_estimator_

        joblib.dump(clf, 'svm_model_silk_N%d_a%f.pkl' %(N,a))

        print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':


    #defining the options of the script

    #INPUTS: -i duke_config.xml, -N number_of_configurations, -a amplitude_of_perturbation, -g gold_standard_name

    parser = optparse.OptionParser()
    parser.add_option('-i','--input', dest = 'file_name', help = 'file_name')
    parser.add_option('-N','--number', dest = 'N', help = 'number of classifiers',type = int)
    parser.add_option('-a','--amplitude', dest = 'a', help = 'amplitude of perturbation',type = float)
    parser.add_option('-g','--gold', dest = 'gold_standard_name', help = 'gold_standard_name')
    parser.add_option('-s', '--software', dest = 'software_name', help = 'software name')

    (options, args) = parser.parse_args()

    if options.file_name is None:
       options.file_name = raw_input('Enter file name:')

    if options.N is None:
        options.N = raw_input('Enter number of classifiers:')

    if options.a is None:
        options.a = 0.05 #default to 0.05

    if options.gold_standard_name is None:
        options.gold_standard_name = raw_input('Enter gold standard file name:')

    if options.software_name is None:
        options.software_name = raw_input('Enter software name, silk or duke:')


    file_name = options.file_name #define the variables
    gold_standard_name = options.gold_standard_name
    N = int(options.N)
    a = float(options.a)
    software_name = options.software_name

    stem_serialize = Serializer(file_name,gold_standard_name,N,a)

    if software_name == 'silk':

        stem_serialize.serialize_stem_silk()

    else:

        stem_serialize.serialize_stem_duke()

    

