##################
##### STEM ########
##################

Stacked Threshold-based Entity Matching (STEM) allows to run several instances of unsupervised matchers and use their predictions as a feature vector for an SVM classifier.
The experiments have been conducted using two different base classifier (Duke, Silk) on three datasets (FEIII, 3cixty and DOREMUS).

-Put your configuration file into config/your_experiment
-Put your data sets to match into data/your_experiment
-Put your gold standard file into data/your_experiment/gs


###DUKE

cd STEM/src

-FEIII
python STEM.py -i ../config/FEIII2016/FFIEC_SEC.xml -N 10 -a 0.2 -g ../data/FEIII2016/gs/FFIEC-SEC-GroundTruth.csv -s duke

-3cixty
python STEM.py -i ../config/3cixty/config_duke_3cixty_nice_events.xml -g ../data/3cixty/gs/gs_3cixty_nice_events.csv -N 10 -a 0.2 -s duke

-DOREMUS
 python STEM.py -i ../config/DOREMUS/Config1_duke.xml -N 10 -a 0.2 -g ../data/DOREMUS/Doremus/4-heterogeneities/doremus_gs.csv -s duke


###SILK

cd STEM/src

-FEIII
python STEM.py -i ../config/FEIII2016/FFIEC_SEC_silk.xml -N 10 -a 0.2 -g ../data/FEIII2016/gs/FFIEC-SEC-GroundTruth.csv -s silk

-3cixty
python STEM.py -i ../config/3cixty/config_duke_3cixty_nice_events.xml -g ../data/3cixty/gs/gs_3cixty_nice_events.csv -N 10 -a 0.2 -s silk

-DOREMUS
 python STEM.py -i ../config/DOREMUS/Config1.xml -N 10 -a 0.2 -g ../data/DOREMUS/4-heterogeneities/gs/doremus_gs.csv -s silk

