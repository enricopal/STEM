#####################################################
### STEM: Stacked Threshold-based Entity Matching ###
#####################################################

STEM is a software for entity matching (deduplication, record linkage, link discovery...). It runs several instances of threshold-based classifiers with different threshold values and use their predictions as a feature vector for an SVM classifier.

Two popular threshold-based entity matching systems are supported:

- Duke: https://github.com/larsga/Duke

- Silk: https://github.com/silk-framework/silk
 
STEM requires a configuration file and a gold standard. You also need to specify the number of instances N and the amplitude of perturbation a.

When you start your experiment, you should place the files in the following way:

-configuration_file: STEM/config/my_experiment/config.xml
-gold_standard: STEM/data/my_experiment/gs/gs.csv

Then:

cd STEM/src

STEM-Duke:
python STEM.py -i ../config/my_experiment/config.xml -g ../data/my_experiment/gs/gs.csv -N 10 -a 0.2 -s duke

where config_file.xml is a valid Duke configuration file

STEM-Silk:
python STEM.py -i ../config/my_experiment/config.xml -g ../data/my_experiment/gs/gs.csv -N 10 -a 0.2 -s silk

where config_file.xml is a valid Silk configuration file

The Gold Standard needs to have this format and to be put in a specific folder:
+,id1,id2,1.0
-,id1,id2,1.0
+,id1,id2,1.0

You can also train the model and serialize it:

cd STEM/src

STEM-Duke:
python Serializer.py -i ../config/my_experiment/config.xml -g ../data/my_experiment/gs/gs.csv -N 10 -a 0.2 -s duke

STEM-Duke:
python Serializer.py -i ../config/my_experiment/config.xml -g ../data/my_experiment/gs/gs.csv -N 10 -a 0.2 -s silk

these will generate pickle files (my_model.pkl) that can be loaded without retraining using:

cd STEM/src

STEM-Duke:
python STEM.py -i ../config/my_experiment/config.xml -N 10 -a 0.2 -s duke -m ../models/my_experiment/my_model.pkl

STEM-silk
python STEM.py -i ../config/my_experiment/config.xml -N 10 -a 0.2 -s silk -m ../models/my_experiment/my_model.pkl


The generated output can be in a .csv format:

id1,id2

or .nt format:

<id1> <http://www.w3.org/2002/07/owl#sameAs> <id2>
