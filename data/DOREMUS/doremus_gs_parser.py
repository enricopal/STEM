import optparse

parser = optparse.OptionParser()
parser.add_option('-i','--input', dest = 'input_file_name', help = 'input_file_name')
parser.add_option('-o','--output', dest = 'output_file_name', help = 'output_file_name')

(options, args) = parser.parse_args()

if options.input_file_name is None:
   options.input_file_name = raw_input('Enter input file name:')

if options.output_file_name is None:
    options.output_file_name = raw_input('Enter output file name:')

input_file_name = options.input_file_name
output_file_name = options.output_file_name

f = open(input_file_name,'rU')
out = open(output_file_name,'w')

lines = f.readlines()

for index in range(len(lines) - 1):

    line = lines[index]

    line = line.split('=')
    #select only entities lines
    #<entity1 rdf:resource="http://data.doremus.org/Self_Contained_Expression/F22/cdf710e4-49d2-411f-b1b9-ccfe2a65e258"/>
    if line[0] == '<entity1 rdf:resource':
        #select only the id cdf710e4-49d2-411f-b1b9-ccfe2a65e258
        id1_whole = line[1].replace('\"/>\n','').strip('\"')
        #id1_whole = id1_whole.split('/')
        #id1 = id1_whole[-2].strip('\"')

        #the following line has the other entity

        next_line = lines[index + 1]

        next_line = next_line.split('=')
        
        id2_whole = next_line[1].replace('\"/>\n','').strip('\"')
        #id2_whole = id2_whole.split('/')
        #id2 = id2_whole[-2].strip('\"')

        out.write('+,')
        out.write(id1_whole)
        out.write(',')
        out.write(id2_whole)
        out.write(',1.0')
        out.write('\n')

f.close()
out.close()    
