Documenting the 3cixty entity matching workflow
Each command has to be launched from STEM/src

###############
## GENETIC ####
###############

# WARN: the active mode as instantiated as below rewrites the config_genetic_duke_3cixty_nice_places.xml when resuming after a break
java -cp ../lib/Duke/duke-core/target/*:../lib/Duke/duke-dist/target/*:../lib/Duke/dukeib/Duke/duke-json/target/*:../lib/Duke/duke-lucene/target/*:../lib/Duke/duke-mapdb/target/*:../lib/Duke/duke-mongodb/target/*:../lib/Duke/duke-server/target/*:../lib/Duke/lucene_jar/* no.priv.garshol.duke.genetic.Driver --output=../config/3cixty/config_genetic_duke_3cixty_nice_places.xml --linkfile=../data/3cixty/gs/gs_3cixty_nice_places.csv  --testfile=../data/3cixty/gs/gs_3cixty_nice_places.csv --active ../config/3cixty/config_duke_3cixty_nice_places.xml

####
###### Experiments with Duke
### 

###############
## STACKING ###
###############

Three alternative approaches:

1) train the model and obtain scores

python STEM.py -i ../config/3cixty/config_duke_3cixty_nice_places.xml -g ../data/3cixty/gs/gs_3cixty_nice_places.csv -N 10 -a 0.2 -s duke --rdf

2) pretrain the model and then load it, without scoring

python Serializer.py -i ../config/3cixty/config_duke_3cixty_nice_places.xml -g ../data/3cixty/gs/gs_3cixty_nice_places.csv -N 10 -a 0.2 -s duke

python STEM.py -i ../config/3cixty/config_duke_3cixty_nice_places.xml -m ../models/3cixty/svm_model_duke_N10_a0.2.pkl -N 10 -a 0.2 -s duke --rdf

3) use a pretrained model with scoring

python STEM.py -i ../config/3cixty/config_duke_3cixty_nice_places.xml -m ../models/3cixty/svm_model_duke_N10_a0.2.pkl -N 10 -a 0.2 -s duke --rdf -g ../data/3cixty/gs/gs_3cixty_nice_places.csv


#################
## NO STACKING ##
#################

java -cp ../lib/Duke/duke-core/target/*:../lib/Duke/duke-dist/target/*:../lib/Duke/duke-es/target/*:../lib/Duke/duke-json/target/*:../lib/Duke/duke-lucene/target/*:../lib/Duke/duke-mapdb/target/*:../lib/Duke/duke-mongodb/target/*:../lib/Duke/duke-server/target/*:../lib/Duke/lucene_jar/* no.priv.garshol.duke.Duke --showmatches ../config/3cixty/config_genetic_duke_3cixty_nice_places.xml > /tmp/output.txt

python parser/parser.py -s duke -i /tmp/output.txt -o /tmp/output_parsed.csv --id1 ID1 --id2 ID2
python scorer/scorer.py -i /tmp/output_parsed.csv -g ../data/3cixty/gs/gs_3cixty_nice_places.csv



####
###### Experiments with SILK
### 

###############
## STACKING ###
###############

python STEM.py -i ../config/3cixty/config_silk_3cixty_nice_places.xml -g ../data/3cixty/gs/gs_3cixty_nice_places.csv -N 5 -a 0.2 -s silk

#################
## NO STACKING ##
#################

java -Xmx5000m -DconfigFile=../config/3cixty/config_silk_3cixty_nice_places.xml -Dthreads=4 -jar ../lib/Silk/silk.jar 
python parser/parser.py -s silk -i ../data/3cixty/places_accepted_links.nt -o /tmp/output_parsed.csv --id1 ID1 --id2 ID2
python scorer/scorer.py -i /tmp/output_parsed.csv -g ../data/3cixty/gs/gs_3cixty_nice_places.csv
