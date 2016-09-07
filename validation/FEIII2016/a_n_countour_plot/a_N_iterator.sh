#!/bin/bash 

echo This script applies STEM with different a and N values;

#rm -f sfem_validation_results.csv ;

for a in 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4; do 
  echo perturbation amplitude $a; 
  for N in 5 10 15 20 25 50 75 100; do 
    echo number of configuration $N;
    cd ../../../src
    output_stem=`python STEM.py -s duke -N $N -a $a -i ../config/FEIII2016/FFIEC_SEC.xml -g ../data/FEIII2016/gs/FFIEC-SEC-GroundTruth.csv`;
    echo $N,$a,$output_sfem >> STEM_a_N.csv;
  done;
done;
