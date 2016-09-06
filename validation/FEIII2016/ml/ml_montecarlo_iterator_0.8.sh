#!/bin/bash
rm -f ml_validation_results.csv ;

for fold in 0.8 ; do 
  
  echo foreach $fold of the Training Set ; 
  
  for file in `ls -v ../GS/$fold`; do 

    out=/tmp/out_ml_validation.csv;
    echo "FFIEC_ID,SED_ID,NAME,ADDRESS,CITY,STATE,y">$out;

    echo "Parsing dataset $file"
    while read -r line
    do
        y=`echo $line | cut -d"," -f1`;
        if [ "$y" = "+" ]; then
            y_boolean=1;
        else
            y_boolean=0;
        fi

        id1=`echo $line | cut -d"," -f2`;
        id2=`echo $line | cut -d"," -f3`;
        

        sim_out=`java -cp ../../../lib/Duke/duke-core/target/*:../../../lib/Duke/duke-dist/target/*:../../../lib/Duke/duke-es/target/*:../../../lib/Duke/duke-json/target/*:../../../lib/Duke/duke-lucene/target/*:../../../lib/Duke/duke-mapdb/target/*:../../../lib/Duke/duke-mongodb/target/*:../../../lib/Duke/duke-server/target/*:../../../lib/Duke/lucene_jar/* no.priv.garshol.duke.MachineLearningSimilarities ../../../config/FEIII2016/FFIEC_SEC_no_blocking.xml $id1 $id2`;
        sim_out_clean=`echo $sim_out | sed -r 's/.{26}//'`;

        echo "$id1,$id2,$sim_out_clean$y_boolean" >> $out; 
    done < ../GS/$fold/$file

    echo $file;
    output_ml=`python ml_validation.py -g $out`;
    echo $fold,$output_ml >> ml_validation_results_0.8.csv;
  done;
done;