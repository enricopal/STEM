#the construction of the doremus gs starts from the refalign.rdf file

python doremus_gs_parser.py -i refalign.rdf -o doremus_gs.csv

#then, in order to provide also negative instances to the learning algorithm negative instances are added
#this is done by looking up the output of a silk run (output.nt) and checking if the pair is annotated in the gs
#if it's not annotated, then it's a negative instance and it is added to the gs

python add_negative_examples.py -i output_silk.nt -g doremus_gs.csv -o doremus_gs_with_negative_examples.csv