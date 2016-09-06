import optparse
from collections import defaultdict
import numpy as np


def silk_output_parser(input_file_name,output_file_name,id1,id2):

  input_read = open(input_file_name,'rU') #read input file
  train = open(output_file_name,'w') #write on output file

    #write the headers
  train.write(id1)
  train.write(',')
  train.write(id2)
  train.write('\n')

  k = 0 #counter
      
      #file to parse
      #<http://dbpedia.org/resource/Where_Are_My_Children%3F>  <http://www.w3.org/2002/07/owl#sameAs>  <http://data.linkedmdb.org/resource/film/236> 

  for line in input_read.readlines(): #iterate through the lines of the file
      
      line = line.split(' ') #split when there's a space
      
      if line[0] == 'End': #we need to pass to the next configuration
          k += 1
          continue

      ID1_whole = line[0] #<http://dbpedia.org/resource/Where_Are_My_Children%3F>, first element of the list
      ID2_whole = line[-2] #<http://data.linkedmdb.org/resource/film/236> , second last element of the list

      #ID1_whole = ID1_whole.split('/')
      #ID2_whole = ID2_whole.split('/')

      ID1 = ID1_whole.strip('<').strip('>') 
      ID2 = ID2_whole.strip('<').strip('>') 

      train.write(ID1)
      train.write(',')
      train.write(ID2)
      train.write('\n')

  train.close()


#execute as a script
if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-i','--input', dest = 'input_file_name', help = 'input_file_name')
    parser.add_option('-o','--output', dest = 'output_file_name', help = 'output_file_name')
    parser.add_option('-u','--id1', dest = 'id1', help = 'id1')
    parser.add_option('-k','--id2', dest = 'id2', help = 'id2')


    (options, args) = parser.parse_args()

    if options.input_file_name is None:
       options.input_file_name = raw_input('Enter input file name:')

    if options.output_file_name is None:
        options.output_file_name = raw_input('Enter output file name:')

    if options.id1 is None:
        options.id1 = raw_input('Enter identifier of the first column (e.g. FFIEC_ID):')

    if options.id2 is None:
        options.id2 = raw_input('Enter identifier of the second column (e.g. SEC_ID):')

    input_file_name = options.input_file_name
    output_file_name = options.output_file_name
    id1 = options.id1
    id2 = options.id2

    silk_output_parser(input_file_name,output_file_name,id1,id2) 