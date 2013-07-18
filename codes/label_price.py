from itertools import izip, tee
from dateutil.parser import parse
import os 
import numpy as np
import cPickle

price_path = "/home/jadidi/python-workespace/DataMinig_Lab/src/Data/prices/sp100"
output_path = "/home/jadidi/python-workespace/DataMinig_Lab/src/result/s&p"

class LabelPrices(object):
    def __init__(self,threshold):
        self.threshold = threshold
        
    def _pairwise(self, iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = tee(iterable)
        next(b, None)
        return izip(a, b)
    
    def _save(self, record, file_name):
        """ write dictionary to file, key = date, value = (price_change, labels) """ 
        dic = {}
        for date, pchange, label in record:
            dic[date] = (pchange ,label)
        cPickle.dump(dic,open("{0}/DL_{1}.p".format(output_path,file_name[:-4]),"wb"))
        
    def _combineDateChangeLabel(self, date, price_change,label):
        """combine date price_change and label for each entry """
        return izip(date, price_change, label)
    
    def _calcLabel(self, price_change):
        """ calculate the label based on given threshold"""
        labels = ["-1" if abs(g) >= self.threshold and g<0 
                  else "1" if abs(g) >= self.threshold and g>0 
                  else "0" for g in price_change] 
        return labels
     
    def _priceChange(self, price_list):
        """calculate relative price changes """
        pr_changes = [100*((y-x)/y) for x,y in self._pairwise(price_list)]
        return pr_changes
    
    def _formatDates(self, date_list):
        """
        change the date format to desired one.i.e '20000103' -> '2000-01-03'         
        """
        dates = map(lambda x:parse(x).strftime("%Y-%m-%d") ,date_list)
        return dates
    
    def _process(self,price_file):
        file_name = "{0}/{1}".format(price_path,price_file)
        data =  np.loadtxt(file_name, dtype= "object")
        price_list =  data[:,4].astype(np.float32)
        date_list = data[:,0]
        
        price_change = self._priceChange(price_list)
        labels = self._calcLabel(price_change)
        dates = self._formatDates(date_list)
        record = self._combineDateChangeLabel(dates,price_change,labels)
        self._save(record, price_file)
        
        
        
    

def main():
    price_data =os.listdir(price_path)
    LP = LabelPrices(2) 
    for fname in price_data:
        LP._process(fname)
        
    print "Done!"    
if __name__ == "__main__":
    main()