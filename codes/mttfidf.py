import numpy as np
from data_cleaner import data_cleaner

global_terms_in_doc = {}
global_term_freq = {}

def TF(terms):
    terms_in_doc = {}
    for term in terms:
        try:
            counts = terms.count(term)
            terms.remove(term)
            terms_in_doc[term] = counts
            global_term_freq[term] +=1
        except:
            terms_in_doc[term] = 1   
            global_term_freq[term] = 1 
    return terms_in_doc

def IDF(n_doc):
    IDF_terms_in_docs = {}
    for term,freq in global_term_freq.items():
        IDF_terms_in_docs[term]  = np.log(float(n_doc) / (1+freq))      
    return IDF_terms_in_docs
    

def TFIDF(n_doc):
    result =[]
    idf_dict = IDF(n_doc)
    for i in range(n_doc):
            for term, freq in global_terms_in_doc[i].items():
                tfidf = freq * idf_dict[term]
                result.append([tfidf, term])    
    result = sorted(result,reverse= True)
    return result

def write_to_file(result):
    writer = open("result/2011-03-25"+ '_tfidf', 'w')    
    for (tfidf, term) in result:
        writer.write(term + '\t\t' + str(tfidf) + '\n')
    writer.close()
    
def main():
    dc = data_cleaner()
    data = np.loadtxt("reuters/2011-03-25",dtype=np.object,delimiter="\t")
    data =data[:,2]
    row_number = 0
    n_doc = 5
    
    for news in data[0:n_doc]:
        news_terms = dc._clean(news)
        global_terms_in_doc[row_number] = TF(news_terms)
        row_number+=1   
                    
    tfidf = TFIDF(n_doc)
    write_to_file(tfidf)
    

if __name__ == "__main__":
    main()


