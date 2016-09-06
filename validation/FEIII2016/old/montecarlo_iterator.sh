#!/bin/bash 

for f in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9; do 
  echo Slice $f of the Training Set ; 
  python training_size_T2_experiment.py -i training_set_T2_n1000.csv -f $f -T 1000 ;
done