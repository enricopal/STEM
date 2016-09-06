import optparse

#Parse the raw output of Duke and creates a .csv file with ID1,ID2 as columns and True Positives as rows

def duke_output_parser(input_file_name,output_file_name,id1,id2):

      input_read = open(input_file_name,'rU') #read input file
      train = open(output_file_name,'w') #write on output file

      #write the headers
      train.write(id1)
      train.write(',')
      train.write(id2)
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

    duke_output_parser(input_file_name,output_file_name,id1,id2)



