import numpy as np
import os 
from dateutil.parser import parse
import cPickle
import datetime
from collections import defaultdict

#------
from data_cleaner import data_cleaner
import make_price_dict as mpd


no_news = []
no_price = []
words_with_labels = defaultdict(list)
INTERVAL = 1 #day
threshold = 5
begin = "2010-01-01"
stop = "2012-11-02"

news_path = "Data/bloomberg"
#price_path = "Data/prices/indiv"
price_path = "Data/prices/sp100"

def price_change(p1,p2):
    
    return 100*((p1-p2)/p2)


def calc_label(start_time, end_time):
    init_price = price_dict[start_time][3]
    end_price = price_dict[end_time][3]
    p_change = price_change(init_price,end_price)
    label =0
    if p_change < 0 and abs(p_change) > threshold:
        label = -1
    elif p_change > 0 and abs(p_change) > threshold:
        label = 1    
    
    return label

def process_txt(data):
        start_time = parse(data[1])
        end_time = start_time + datetime.timedelta(days= INTERVAL)
        start_time = start_time.strftime("%Y-%m-%d")
        end_time = end_time.strftime("%Y-%m-%d")  
        return  start_time, end_time  

def main():
    
    news_files = os.listdir(news_path)
    comp_price_data =os.listdir(price_path)
    dc = data_cleaner()    
   
    for comp_price in comp_price_data:
        print comp_price
        writer = open("result/s&p/{0}".format(comp_price.split(".")[0]), 'w')
        global price_dict  
        price_dict= mpd.process_txt(comp_price,price_path)
        for news in news_files:
            news_data = open("{0}/{1}".format(news_path,news),"r")
            news_data = news_data.readlines()
            if news_data:
                for row in news_data:
                    record =row.split("\t")
                    start_time, end_time = process_txt(record)
                    try:
                        label = calc_label(start_time, end_time)
                    except:
                        no_price.append((start_time,end_time))
                        #label = "Unk"
                    try:
                        terms = dc._clean(record[2])
             #          words_with_labels[label].append(terms)
                        writer.write(("{0}\t{1}\t{2}\n").format(start_time,terms, label))
                    except Exception:
                        no_news.append(start_time)              
                        continue
            else:
                print "empty news: %s" %news
                continue
            
            #cPickle.dump(no_news,open("no_news_dates.p","wb") )    

            
            cPickle.dump(no_news,open("no_news_dates.p","wb") )    
            cPickle.dump(no_news,open("no_price_dates.p","wb") )    
    

if __name__ == "__main__":
    main()