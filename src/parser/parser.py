import optparse
from collections import defaultdict
import numpy as np


class Parser:

    def __init__(self,input_file_name,output_file_name,id1,id2):
           self.input_file_name = input_file_name
           self.output_file_name = output_file_name
           self.id1 = id1
           self.id2 = id2

    def duke_output_parser(self):

          input_read = open(self.input_file_name,'rU') #read input file
          train = open(self.output_file_name,'w') #write on output file

          #write the headers
          train.write(self.id1)
          train.write(',')
          train.write(self.id2)
          train.write('\n')

          match = 0 #counter

          #this does the same job of the duke2feiii_T1.pl

          for line in input_read.readlines():
              line = line.split(' ') #split when there's a space
              
              if line[0] == 'MATCH': #if a match was found
                  match = 1
                  continue #jump to the next iteration

              if match == 1: #MATCH was found one line above
                 train.write(line[1].replace('\'','')) 
                 match = 2
                 continue 

              if match == 2: #MATCH was found two line above
                 train.write(line[1].replace('\'','').strip(','))
                 train.write('\n')
                 match = 0
                 continue
              
          input_read.close()
          train.close()

    def silk_output_parser(self,prefix):

          input_read = open(self.input_file_name,'rU') #read input file
          train = open(self.output_file_name,'w') #write on output file
          pref = prefix

            #write the headers
          train.write(self.id1)
          train.write(',')
          train.write(self.id2)
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

              ID1 = ID1_whole.strip('<').strip('>') 
              ID2 = ID2_whole.strip('<').strip('>') 


              if pref == 'no':

                 ID1 = ID1.split('/')
                 ID2 = ID2.split('/')

                 ID1 = ID1[-1]
                 ID2 = ID2[-1]


              train.write(ID1)
              train.write(',')
              train.write(ID2)
              train.write('\n')

          train.close()

if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-i','--input', dest = 'input_file_name', help = 'input_file_name')
    parser.add_option('-o','--output', dest = 'output_file_name', help = 'output_file_name')
    parser.add_option('-u','--id1', dest = 'id1', help = 'id1')
    parser.add_option('-k','--id2', dest = 'id2', help = 'id2')
    parser.add_option('-s', '--software', dest='software_name', help = 'software name')
    parser.add_option('-p', '--prefix', dest='prefix', help = 'enter no if you dont want to use the prefix http')


    (options, args) = parser.parse_args()

    if options.input_file_name is None:
       options.input_file_name = raw_input('Enter input file name:')

    if options.output_file_name is None:
        options.output_file_name = raw_input('Enter output file name:')

    if options.id1 is None:
        options.id1 = raw_input('Enter identifier of the first column (e.g. FFIEC_ID):')

    if options.id2 is None:
        options.id2 = raw_input('Enter identifier of the second column (e.g. SEC_ID):')

    if options.software_name is None:
        options.software_name = raw_input('Enter duke or silk')

    input_file_name = options.input_file_name
    output_file_name = options.output_file_name
    id1 = options.id1
    id2 = options.id2
    software_name = options.software_name
    prefix = options.prefix


    if software_name == 'silk' or software_name == 'Silk':

        parser = Parser(input_file_name,output_file_name,id1,id2)

        parser.silk_output_parser(prefix) 

    else:
        parser = Parser(input_file_name,output_file_name,id1,id2)

        parser.duke_output_parser()


