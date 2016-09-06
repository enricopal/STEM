#this script is meant to add negative instances to the doremus gs
#negative instances are necessary for the learning process of SEM
#this is obtained by parsing the output of silk and looking up the gs. if the ids are not there, they are written in concat as negative examples

import optparse
from collections import defaultdict
import numpy as np

parser = optparse.OptionParser()
parser.add_option('-i','--input', dest = 'input_file_name', help = 'input_file_name')
parser.add_option('-g','--gold', dest = 'gold_standard_name', help = 'gold_standard_name')
parser.add_option('-o','--output', dest = 'output_file_name', help = 'output_file_name')

(options, args) = parser.parse_args()

if options.input_file_name is None:
   options.input_file_name = raw_input('Enter input file name:')

if options.output_file_name is None:
    options.output_file_name = raw_input('Enter output file name:')

if options.gold_standard_name is None:
    options.gold_standard_name = raw_input('Enter gold standard file name:')

input_file_name = options.input_file_name
output_file_name = options.output_file_name
gold_standard_name = options.gold_standard_name

input_read = open(input_file_name,'rU') #read input file
negative_examples = open(output_file_name,'w') #write on output file
gold_standard_read = open(gold_standard_name,'rU')

match_dict = {} #for each pair id1,id2 the list of configuration where it is found as integer k
gold_standard = {}

  #here we build a dictionary containing the gold_standard, (id1,id1) : 1 or 0

for i in gold_standard_read.readlines():
    i = i.split(',') #split at commas
    if i[0] == '+': #TP
       gold_standard[(i[1],i[2])] = 1
    elif i[0] == '-': #FP
       gold_standard[(i[1],i[2])] = 0

  ##dictionary: {(id1,id2) : [list_of_configuration_where_the_match_is_found]}
  
  #file to parse
  #<http://dbpedia.org/resource/Where_Are_My_Children%3F>  <http://www.w3.org/2002/07/owl#sameAs>  <http://data.linkedmdb.org/resource/film/236> 
  
for line in input_read.readlines(): #iterate through the lines of the file
      
      line = line.split(' ') #split when there's a space

      ID1_whole = line[0] #<http://dbpedia.org/resource/Where_Are_My_Children%3F>, first element of the list
      ID2_whole = line[-2] #<http://data.linkedmdb.org/resource/film/236> , second last element of the list

      #ID1_whole = ID1_whole.split('/')
      #ID2_whole = ID2_whole.split('/')

      ID1 = ID1_whole.strip('>').strip('<') 
      ID2 = ID2_whole.strip('>').strip('<') 
      
      match_dict[(ID1,ID2)] = 1

for i,j in match_dict.keys():
    try:
        print gold_standard[i,j]

    except KeyError:
        negative_examples.write('-,%s,%s,1.0\n' %(i,j))

negative_examples.close() 