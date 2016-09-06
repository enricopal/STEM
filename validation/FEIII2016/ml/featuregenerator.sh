#!/bin/bash
tail -n +2 ../../../data/FEIII2016/Data\ and\ Metadata/FFIEC.csv > /tmp/ds1;
ds1=/tmp/ds1;

tail -n +2 ../../../data/FEIII2016/Data\ and\ Metadata/SEC.csv > /tmp/ds2;
ds2=/tmp/ds2;

out=gs.csv;
echo "FFIEC_ID,SED_ID,NAME,ADDRESS,CITY,STATE,y">$out;

echo "Parsing dataset ../../../data/FEIII2016/Data\ and\ Metadata/FFIEC.csv"
while read -r line1
do
    echo "Parsing dataset ../../../data/FEIII2016/Data\ and\ Metadata/SEC.csv"
    while read -r line2
    do
    	id1=`echo $line1 | cut -d"," -f1`;
    	id2=`echo $line2 | cut -d"," -f1`;
    	#echo -e "$val1,$val2";

    	## launch the script ##
        sim_out=`java -cp ../../../lib/Duke/duke-core/target/*:../../../lib/Duke/duke-dist/target/*:../../../lib/Duke/duke-es/target/*:../../../lib/Duke/duke-json/target/*:../../../lib/Duke/duke-lucene/target/*:../../../lib/Duke/duke-mapdb/target/*:../../../lib/Duke/duke-mongodb/target/*:../../../lib/Duke/duke-server/target/*:../../../lib/Duke/lucene_jar/* no.priv.garshol.duke.MachineLearningSimilarities ../../../config/FEIII2016/FFIEC_SEC_no_blocking.xml $id1 $id2`;

        sim_out_clean=`echo $sim_out | sed -r 's/.{26}//'`;
        
        y=`python gs_lookup.py -g ../../../data/FEIII2016/ground\ truth/FFIEC-SEC-GroundTruth.csv --id1 $id1 --id2 $id2`;   
        #y=`echo 0`;
       
        if [ "$y" -ne -1 ]; then
        	echo "$id1,$id2,$sim_out_clean$y" >> $out; 
        fi

    done < "$ds2"
done < "$ds1"