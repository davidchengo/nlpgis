'''
Created on Nov 27, 2012

@author: davidchen
'''


from nltk.corpus import brown
from nltk import *

def lexical_diversity(text):
    return len(text) / len(set(text))
def percentage(count, total):
    return "%.2f" % (100.0 * count / total)

if __name__ == '__main__':
    brown.categories()
    spatial_token=set()
    with open("../ontology/Token","r") as fr:
        fr.readline()
        for line in fr:
            spatial_token.add(line.split("|")[1])
    print spatial_token
    with open("../ontology/frequency_sum_brown","w") as fw1:
        fw1.write("ID|Token|AvgFreq\n")
        with open("../ontology/frequency_brown","w") as fw2:
            count=0
            fw2.write("ID|Book|Token|Freq\n")
            for token in spatial_token:
                count+=1
                for category in brown.categories():
                    text=Text(brown.words(categories=category))
                    sum=float(percentage(text.count(token),len(text)))
                    fw2.write("%d|%s|%s|%s\n" % (count,category,token,percentage(text.count(token),len(text))))
                fw1.write("%d|%s|%.2f\n" % (count,token,sum/9))
                print count
                
    