import os
from collections import defaultdict
from dateutil.parser import parse
import cPickle
from collections import Counter
#--------------------------My Functions----------------------------- 
from data_cleaner import DataCleaner

#===============================================================================
# Define Golbal Variable
#===============================================================================
news_path = "/home/jadidi/python-workespace/DataMinig_Lab/src/Data/bloomberg"
dates_words_dict = defaultdict(set)
#d = defaultdict(lambda: defaultdict(int))
dc = DataCleaner() 


def makeDateFormat(record):
    """extract date of news and change its format.  """
    date = parse(record[1])
    return date.strftime("%Y-%m-%d")
    
def processData(data):
    """extract, clean, store words in the news. """
    record = data.split("\t")
    date = makeDateFormat(record)
    terms = set(dc._clean(record[2]))
    dates_words_dict[date].update(terms)

def saveDict():
    """dump dictionary to disk.  """
    cPickle.dump(dates_words_dict,open("dates_words_dict.p","wb"))
    
def main():
    news_files = sorted(os.listdir(news_path))
    for news in news_files:
        print news
        try:
            # if news file is not empty 
            news_data = open("{0}/{1}".format(news_path,news),"r")
            for row in news_data:
                processData(row)
            news_data.close()
        except Exception, e:
            print e
            pass
     
    saveDict()         
    
if __name__ == "__main__":
    main()
