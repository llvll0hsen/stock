# -*- coding: utf-8 -*-
import numpy as np
from nltk.corpus import stopwords
import string
import re       
import nltk.stem.porter as pStemmer

class data_cleaner(object):
    def __init__(self):
        self.stopwords = stopwords.words('english')

    def _removeDateFromNews(self,txt):
        sep="EDT"
        result = ""
        try:
            result = txt.split(sep,1)[1]
        except Exception :
            print txt
                
        return result
    
    def _removeURLs(self,txt):
        """remove urls"""
        p = re.compile(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', re.DOTALL)
        result = re.sub(p, '', txt)
        return result
    
    def _removeEmails(self,txt):
        """remove Email adresses """ 
        result = re.sub(r'[\w\.-]+@[\w\.-]+',"",txt)
        return result
    
    def _removePunc(self,txt):
        """remove punctuations"""
        table = string.maketrans("","")
        result = txt.translate(table, string.punctuation)
        return result
    
    def _removeASCII(self,txt):
        """remove ascci characters"""
        result = re.sub('[^A-Za-z0-9]+', ' ', txt)
        return result
     
    def _removeStopwords(self,txt):    
        """remove stop words"""
        
        result = [w.lower() for w in txt.split() if w.lower().strip() not in self.stopwords]
        return result

    def _removeDigits(self,txt):
        result =  txt.translate(None, string.digits)
        return result
        
    def _removeLenOne(self,txt):
        result = [w for w in txt if len(w)>2]
        return result
    
    def _stemmer(self,txt):
        result = map(lambda w: pStemmer.PorterStemmer().stem(w), txt)
        return result
    
    def _clean(self,txt):
        #no_date = self._removeDateFromNews(txt)
        no_date = txt
        no_url = self._removeURLs(no_date)
        no_emails = self._removeEmails(no_url)
        no_ASCII = self._removeASCII(no_emails)
        no_punc = self._removePunc(no_ASCII)
        no_digit = self._removeDigits(no_punc)
        no_stopwords = self._removeStopwords(no_digit)
        stemmed = self._stemmer(no_stopwords)
        final_result = self._removeLenOne(stemmed)
        return final_result
        
    
def main():
    import os
    print os.listdir("reuters")
    tc = data_cleaner()
    data = np.loadtxt("reuters/2011-03-25",dtype=np.object,delimiter="\t")
    t =data[0]
    
    
    for i in range(20):
        print "*****"
        print tc._clean(t[i])
    
if __name__== '__main__':
    main()



