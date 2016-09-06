import numpy as np
import pandas as pd
import optparse

#INPUTS: gold_standard and output file

def scorer(file_name,gs):

  file_input = open(file_name,'rU') #output of the algorithm

  gold = open(gs,'r') #gold standard

  #building dictionaries with key = (id1,id2) and value = '+' or '-'

  output = {}

  gold_standard = {}

  for i in file_input.readlines():
      i = i.strip('\n')
      
      j = i.split(',') #separate id1 and id2, respectively j[0] and j[1]
      output[(j[0],j[1])] = '+' #in the output file only the positive matches are reported

  for i in gold.readlines():
      j = i.split(',')
      gold_standard[(j[1],j[2])] = j[0] #customized to the gs format of duke goldstandard +,id1,id2,1.0

  #print output.keys()

  #computing precision
  precision = 0

  correct = 0
  wrong = 0

  for id1,id2 in output.keys():

      try:
          if gold_standard[(id1,id2)] == '+': #true positive
             correct += 1

          if gold_standard[(id1,id2)] == '-': #false positive
             wrong += 1 
             

      except KeyError: #not all the keys in the output are in the gold standard and viceversa

          pass

  #print len(output.keys())
  precision = (1.*correct)/(correct + wrong)

  #computing recall

  total_matches = sum([i=='+' for i in gold_standard.values()]) #computing the positive examples in the gold standard
  found_matches = 0

  for id1,id2 in gold_standard.keys():
       
      if gold_standard[(id1,id2)] == '+': #only select positive matches 

         try:
             if output[(id1,id2)] == '+':
                found_matches += 1
         except KeyError:
             pass

  recall = (1.*found_matches)/total_matches

  #computing f-score

  f_score = 2*(precision*recall)/(precision+recall)

  print '\n'
  print 'Precision: ', precision, '\n'
  print 'Recall: ', recall, '\n'
  print 'F-score: ', f_score, '\n'

  file_input.close()
  gold.close()

#INPUTS: gold_standard and output file

def scorer_return(file_name,gs):

  file_input = open(file_name,'rU') #output of the algorithm

  gold = open(gs,'r') #gold standard

  #building dictionaries with key = (id1,id2) and value = '+' or '-'

  output = {}

  gold_standard = {}

  for i in file_input.readlines():
      i = i.strip('\n')
      
      j = i.split(',') #separate id1 and id2, respectively j[0] and j[1]
      output[(j[0],j[1])] = '+' #in the output file only the positive matches are reported

  for i in gold.readlines():
      j = i.split(',')
      gold_standard[(j[1],j[2])] = j[0] #customized to the gs format of duke goldstandard +,id1,id2,1.0

  #print output.keys()

  #computing precision
  precision = 0

  correct = 0
  wrong = 0

  for id1,id2 in output.keys():

      try:
          if gold_standard[(id1,id2)] == '+': #true positive
             correct += 1

          if gold_standard[(id1,id2)] == '-': #false positive
             wrong += 1 
             

      except KeyError: #not all the keys in the output are in the gold standard and viceversa

          pass

  #print len(output.keys())
  precision = (1.*correct)/(correct + wrong)

  #computing recall

  total_matches = sum([i=='+' for i in gold_standard.values()]) #computing the positive examples in the gold standard
  found_matches = 0

  for id1,id2 in gold_standard.keys():
       
      if gold_standard[(id1,id2)] == '+': #only select positive matches 

         try:
             if output[(id1,id2)] == '+':
                found_matches += 1
         except KeyError:
             pass

  recall = (1.*found_matches)/total_matches

  #computing f-score

  f_score = 2*(precision*recall)/(precision+recall)

  file_input.close()
  gold.close()
  
  return precision, recall, f_score


if __name__ == '__main__':
  #defining the options of the script
  parser = optparse.OptionParser()
  parser.add_option('-i','--input', dest = 'file_name', help = 'output_file')
  parser.add_option('-g','--gold', dest = 'gs', help = 'gold_standard')


  (options, args) = parser.parse_args()

  if options.file_name is None:
     options.file_name = raw_input('Enter file name:')

  if options.gs is None:
     options.gs = raw_input('Enter gold_standard file name:')

  file_name = options.file_name #define the name string of the file
  gs = options.gs #define the name string of the gold standard

  scorer(file_name,gs)
