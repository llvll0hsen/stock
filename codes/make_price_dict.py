# -*- coding: utf-8 -*-
import os
from dateutil.parser import parse
import csv

price_path = "Data/prices/sp100"
price_path2 = "Data/prices/indiv"

def process_csv(dfile,path,skipHeader=True):
    with open("{0}/{1}".format(path,dfile),"rb") as fin:
        rows = csv.reader(fin)
        if skipHeader:
            next(rows,None) #skip the header
        d = {parse(row[0],dayfirst=True).strftime("%Y-%m-%d"): row[1:] for row in rows}
    return d    

def process_txt(dfile,path):
    with open("{0}/{1}".format(path,dfile)) as fin:
        rows = ( line.split() for line in fin )
        d = { parse(row[0]).strftime("%Y-%m-%d"):row[1:] for row in rows if parse(row[0])>parse("2010-01-01")}
        
    return d    

def main():
    companies_data =os.listdir(price_path2)
    d=process_csv(companies_data[0],price_path2)
    print d["2010-09-05"]
    
        
if __name__=="__main__":
    main()