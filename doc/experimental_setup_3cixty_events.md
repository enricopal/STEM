Documenting the 3cixty entity matching workflow
Each command has to be launched from STEM/src

###############
## GENETIC ####
###############

## first time
java -cp ../lib/Duke/duke-core/target/*:../lib/Duke/duke-dist/target/*:../lib/Duke/dukeib/Duke/duke-json/target/*:../lib/Duke/duke-lucene/target/*:../lib/Duke/duke-mapdb/target/*:../lib/Duke/duke-mongodb/target/*:../lib/Duke/duke-server/target/*:../lib/Duke/lucene_jar/*:../lib/Duke/spatial4j-0.3.jar no.priv.garshol.duke.genetic.Driver --output=../config/3cixty/config_duke_3cixty_nice_events.xml --linkfile=../data/3cixty/gs/gs_3cixty_nice_events.csv ../config/3cixty/config_duke_seed_3cixty_nice_events.xml

## from the 2nd time on to resume the old activity
java -cp ../lib/Duke/duke-core/target/*:../lib/Duke/duke-dist/target/*:../lib/Duke/dukeib/Duke/duke-json/target/*:../lib/Duke/duke-lucene/target/*:../lib/Duke/duke-mapdb/target/*:../lib/Duke/duke-mongodb/target/*:../lib/Duke/duke-server/target/*:../lib/Duke/lucene_jar/*:../lib/Duke/spatial4j-0.3.jar no.priv.garshol.duke.genetic.Driver --output=../config/3cixty/config_duke_3cixty_nice_events.xml --linkfile=../data/3cixty/gs/gs_3cixty_nice_events.csv  --testfile=../data/3cixty/gs/gs_3cixty_nice_events.csv --active ../config/3cixty/config_duke_seed_3cixty_nice_events.xml

####
###### Experiments with Duke
### 

###############
## STACKING ###
###############

python STEM.py -s duke -i ../config/3cixty/config_duke_3cixty_nice_events.xml -g ../data/3cixty/gs/gs_3cixty_nice_events.csv -N 5 -a 0.2

#################
## NO STACKING ##
#################

java -cp ../lib/Duke/duke-core/target/*:../lib/Duke/duke-dist/target/*:../lib/Duke/duke-es/target/*:../lib/Duke/duke-json/target/*:../lib/Duke/duke-lucene/target/*:../lib/Duke/duke-mapdb/target/*:../lib/Duke/duke-mongodb/target/*:../lib/Duke/duke-server/target/*:../lib/Duke/lucene_jar/* no.priv.garshol.duke.Duke --showmatches ../config/3cixty/config_duke_3cixty_nice_events.xml > output.txt

python duke_output_parser.py -i output.txt -o output_parsed.csv --id1 ID1 --id2 ID2
python scorer.py -i output_parsed.csv -g ../data/3cixty/gs/gs_3cixty_nice_events.csv


####
###### Experiments with Silk
### 
