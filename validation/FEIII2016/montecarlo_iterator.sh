#!/bin/bash 

echo This script applies SFEM to each single gold standard sample and save the results to sfem_validation_results.csv;

rm -f sfem_validation_results.csv ;

for fold in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9; do 
  echo Slice $fold of the Training Set ; 
  for file in `ls -v GS/$fold`; do 
    echo $file;
    output_sfem=`python sfem_validation.py -N 10 -a 0.2 -i ../../config/FEIII2016/FFIEC_SEC.xml -g GS/$fold/$file`;
    echo $fold,$output_sfem >> sfem_validation_results.csv;
  done;
done;
