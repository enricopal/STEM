##############
### SILK #####
##############

#run
java -Xmx5000m -DconfigFile=../config/3cixty/config_silk_3cixty_nice_places.xml -Dthreads=4 -jar ../lib/Silk/silk.jar 

#score
python parser/parser.py -i output_silk.nt -o /tmp/output_parsed.csv --id1 ID1 --id2 ID2 -s silk
python scorer/scorer.py -i /tmp/output_parsed.csv -g ../data/3cixty/gs/gs_3cixty_nice_places.csv 