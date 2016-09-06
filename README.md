
# STEM: Stacked Threshold-based Entity Matching 

STEM is a software for entity matching (also known as deduplication, record linkage, link discovery...). STEM can be used to find duplicate records in your database, or to link a database to another by finding identical records. STEM does not implement entity matching from scratch, but it is based on already existing open source entity matching software.
Two alternative threshold-based entity matching systems are supported:

- [Duke] (https://github.com/larsga/Duke)

- [Silk] (https://github.com/silk-framework/silk)

STEM runs several instances of the base entity matcher with different threshold values and use their predictions as a feature vector for an SVM classifier. In this way, STEM is able to achieve high recall and precision at the same time.

##Dependencies

- Java 8
- Python 2.7
- Python libraries: numpy, scikitlearn, pandas, operator, optparse, xml.etree.ElementTree

##Getting started

STEM requires a configuration file of the base classifier and a gold standard. You also need to specify the number of instances N (e.g. 10) and the amplitude of the threshold perturbation a (e.g. 0.2). Try it:

    cd src
    python STEM.py -i ../config/FEIII2016/FFIEC_SEC.xml -g ../data/FEIII2016/gs/FFIEC-SEC-GroundTruth.csv -s duke -N 5 -a 0.2

When starting your own experiment, you need to choose whether you want to use Duke or Silk as a base classifier. Then, you need to produce a valid Duke or Silk configuration file. You also need to create a gold standard, namely a set of annotated matches that STEM will use to learn. 
The Gold Standard needs to have this format:

    +,id1,id2,1.0
    -,id1,id2,1.0
    +,id1,id2,1.0 

where id1 comes from the first set of data and id1 from the second set of data to match. '+' stands for a correct match and '-' for an incorrect match.

You should organize the files in the following way:

- configuration_file: config/my_experiment/config.xml
- gold_standard: data/my_experiment/gs/gs.csv

Then using Duke:

    cd STEM/src

    python STEM.py -i ../config/my_experiment/config.xml -g ../data/my_experiment/gs/gs.csv -N 10 -a 0.2 -s duke

where config_file.xml is a valid Duke configuration file

or using Silk:

    python STEM.py -i ../config/my_experiment/config.xml -g ../data/my_experiment/gs/gs.csv -N 10 -a 0.2 -s silk

where config_file.xml is a valid Silk configuration file

You can also train the model, serialize it and load it in another moment:

    cd STEM/src

    python Serializer.py -i ../config/my_experiment/config.xml -g ../data/my_experiment/gs/gs.csv -N 10 -a 0.2 -s duke

or

    python Serializer.py -i ../config/my_experiment/config.xml -g ../data/my_experiment/gs/gs.csv -N 10 -a 0.2 -s silk

these will generate pickle files (my_model.pkl) that can be loaded without retraining using:

    python STEM.py -i ../config/my_experiment/config.xml -N 10 -a 0.2 -s duke -m ../models/my_experiment/my_model.pkl
or

    python STEM.py -i ../config/my_experiment/config.xml -N 10 -a 0.2 -s silk -m ../models/my_experiment/my_model.pkl

The generated output can be in a .csv format:

    id1,id2

or .nt format by specifying --rdf flag:

    <id1> <http://www.w3.org/2002/07/owl#sameAs> <id2>
