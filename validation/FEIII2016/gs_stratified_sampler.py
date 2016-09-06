import pandas as pd
import optparse

parser = optparse.OptionParser()
parser.add_option('-i','--input', dest = 'file_name', help = 'file_name')
parser.add_option('-f','--fraction', dest = 'fraction', help = 'fraction of file', type = float)
parser.add_option('-T','--times', dest = 'T', help='number of iterations', type = int)

(options, args) = parser.parse_args()

if options.file_name is None:
   options.file_name = raw_input('Enter file name:')

if options.fraction is None:
    options.fraction = raw_input('Enter fraction:')

if options.T is None:
    options.T = 1

file_name = options.file_name #define the variables
f = options.fraction
T = options.T

data = pd.read_csv(file_name)

data_positive = data[data.values[:,0]=='+'] #positive examples

data_negative = data[data.values[:,0]=='-'] #negative examples

num_positive = len(data_positive) #positive examples in the whole training set

num_negative = len(data_negative) #negative examples in the whole training set

num_sample_positive = int(round(f*num_positive)) #number of positive examples in the sample

num_sample_negative = int(round(f*num_negative)) #number of negative examples in the sample

for i in range(T):

    sample_pos = data.sample(n=num_sample_positive) #randomly select positive examples

    sample_neg = data.sample(n=num_sample_negative) #randomly select negative examples

    data_sample = pd.concat([sample_pos,sample_neg])

    data_sample.to_csv('GS/0.1/%s_sample_%.1f_%d.csv' %(file_name,f,i), index = False)