# -*-coding: utf-8 -*-
import numpy as np
from bs4 import BeautifulSoup 
import collections
import os, os.path
import re
from nltk.corpus import stopwords
from nltk import stem
from cPickle import dump
import string
import re

class htmlParser(object):
   
    def __init__(self,path,categories):
        self.path=path
        self.categories=categories
        self.years=range(2004,2006)
        self.months=range(1,13)
        self.days=range(1,31)
       # self.alphabet = list(ascii_lowercase)
        self.stopwords = stopwords.words('english') 
        self.NewsContainer=[]
        self.NCAppend=self.NewsContainer.append
        self.table = string.maketrans("","")
  
    def _removeStopwords(self,news):
        """
        removing stopwords from news
        """
        return [w for w in news if not w in self.stopwords]
    
    def _removePunc(self, news):
        result = re.sub("[\.\t\,\:;\(\)\.]", "", news, 0, 0)
        return result
    
    def _stemmer(self,news):
        stemmer = stem.snowball.EnglishStemmer()
       # stemmed = map(lambda x:stemmer.stem(x), news )
        stemmed = []
        for word in news:
            try:
                stemmed.append(stemmer.stem(word))
            except Exception ,e:
#                print word
                print "*****"
                print e
                
        return stemmed
         
    def _getTimeStamp(self,_soup):
        """
        function to get time stamp (houre,minute,PM/AM)
        input= soup{webpage contents}
        output= (h,m,PM/AM)
        """
        
        try:
            for item in _soup('p',{'class':'publishedDate'}):
                timestamp=item.getText().split()[0]
            
            h,temp=timestamp.split(":") 
            m=int(temp[0:2])
            AP=temp[2:]
            return (int(h),m,AP)
        except Exception, e:
            print "*****"
            print _soup('p',{'class':'publishedDate'})
            pass  


    def _getTitle(self,_soup):
        """
        returning the title of news
        """
        title =_soup.title.getText()
        title = re.compile(re.escape(' -')+ '.*').sub('',title.lower())
        title = self._removePunc(title) 
        return self._stemmer( self._removeStopwords(title.split()) )
                  
    def _getSecondTitle(self,_soup):
        """
        returning second title of news
        """
        secondTitle = ["gerrr"]
        for item in _soup.findAll(attrs={"name":"description"}):
            secondTitle=item['content'].lower()
        secondTitle = self._removePunc(secondTitle).split()
        return self._stemmer( self._removeStopwords(secondTitle) )

    def _getNews(self,_soup):
        """
        first retrieving news content and then removing stopwords 
        """
        newsBody = ["gerrr"]
        for item in _soup('div',{'id':'mainBodyArea'}): 
            newsBody=item.getText().lower()
        
        newsBody = self._removePunc(newsBody).split()
        return self._stemmer( self._removeStopwords(newsBody) )


    def _start(self):
        """
        iterate through folders and get the webpages
        input=
        output= list of webpages for a specific day.

        """
        for y in self.years:
            for m in self.months:
                for d in self.days:
                    for cat in self.categories:
                        directory=self.path+"{0}/{1}/{2}/{3}".format(y,m,d,cat)
                        #print (y,m,d,cat)
                        htmlFiles=[files for files in os.listdir(directory) if files.endswith(".html")]
                        #print len(htmlFiles)
                        self._parser(directory,htmlFiles,(y,m,d),cat)
     
        
        dump(self.NewsContainer,open("parser1.p","wb"))
   
    def _parser(self,directory,htmlFiles,date,category):
        """
        Function to pars html page and make a struct for each and append all struct to list 
        NewsContainer: contain struct for all webpages
        """
        for html in htmlFiles:
            webpage=directory+"/"+html
            print webpage
            print "----------------------"
            soup=BeautifulSoup(open(webpage,'r').read(), 'lxml')
            try:
                timeStamp =self._getTimeStamp(soup)
                title=self._getTitle(soup)
                secondTitle=self._getSecondTitle(soup)
                newsBody=self._getNews(soup)
                self.NCAppend(struct(timeStamp,date,category,title,secondTitle,newsBody))
            except:
                pass

def main():
    
    path="/home/jadidi/crawled/"
    categories=["comment","culture","earth","education","expat","fashion","finance","foodanddrink","gardening","health","motoring","news","property","science","sport","technology","travel","world"]

    parser=htmlParser(path,categories)
    parser._start()


if __name__=="__main__":
   struct = collections.namedtuple('struct','time date category title secondTitle body')
   main()
   

