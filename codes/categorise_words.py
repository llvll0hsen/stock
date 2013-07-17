import numpy as np
import os
import cPickle
from collections import defaultdict
from ast import literal_eval
 
SOURCE = "result/bloomberg"
words_with_labels = defaultdict(list)



def dump_dict(record):
    for row in record:
        words = list(literal_eval(row[1]))
        label = int(float(row[2]))
        words_with_labels[label].append(words)

def main():
    files = os.listdir("{0}".format(SOURCE))
    for f in files:
        try:
            news_data = np.loadtxt("{0}/{1}".format(SOURCE,f),dtype=np.object,delimiter="\t")
            dump_dict(news_data)
        except Exception:
            print f
            pass
        
    print "dump to file"    
    cPickle.dump(words_with_labels,open("result/words_with_lables2.p","wb"))
    print "done"
    
if __name__=="__main__":
    main()