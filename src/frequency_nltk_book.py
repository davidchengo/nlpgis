'''
Created on Nov 27, 2012

@author: davidchen
'''
"""
How can we automatically identify the words of a text that are most informative about
the topic and genre of the text? Imagine how you might go about finding the 50 most
frequent words of a book. One method would be to keep a tally for each vocabulary
item
"""

from nltk import *
from nltk.book import *

"""
*** Introductory Examples for the NLTK Book ***
Loading text1, ..., text9 and sent1, ..., sent9
Type the name of the text or sentence to view it.
Type: 'texts()' or 'sents()' to list the materials.
text1: Moby Dick by Herman Melville 1851
text2: Sense and Sensibility by Jane Austen 1811
text3: The Book of Genesis
text4: Inaugural Address Corpus
text5: Chat Corpus
text6: Monty Python and the Holy Grail
text7: Wall Street Journal
text8: Personals Corpus
text9: The Man Who Was Thursday by G . K . Chesterton 1908
"""

def lexical_diversity(text):
    return len(text) / len(set(text))
def percentage(count, total):
    return "%.2f" % (100.0 * count / total)
if __name__ == '__main__':
    '''Searching Text
There are many ways to examine the context of a text apart from simply reading it. A
concordance view shows us every occurrence of a given word, together with some
context. Here we look up the word monstrous in Moby Dick by entering text1 followed
by a period, then the term concordance, and then placing "monstrous" in parentheses'''
#    text1.concordance("monstrous")
    #text1.similar("near")
    #text1.common_contexts(["monstrous", "very"])
    '''Lexical dispersion plot for words in U.S. Presidential Inaugural Addresses: This can be
used to investigate changes in language use over time.It is one thing to automatically detect that a particular word occurs in a text, and to
display some words that appear in the same context. However, we can also determine
the location of a word in the text: how many words from the beginning it appears. This
positional information can be displayed using a dispersion plot. Each stripe represents
an instance of a word, and each row represents the entire text. In Figure 1-2 we see
some striking patterns of word usage over the last 220 years (in an artificial text constructed
by joining the texts of the Inaugural Address Corpus end-to-end). You can
produce this plot as shown below.'''
    #text4.dispersion_plot(["citizens", "democracy", "freedom", "duties", "America","liberty","constitution"])
    #text3.generate()
    #print len(sorted(set(text3)))
    # calculate a measure of the lexical richness of the text.
    # print len(text3) / len(set(text3))
    # We can count how often a word occurs in a text, and compute what percentage of the text is taken up by a specific word
    #print text3.count("smote")
    #print 100 * text4.count('lol') / len(text5)
    spatial_token=set()
    with open("../ontology/Token","r") as fr:
        fr.readline()
        for line in fr:
            spatial_token.add(line.split("|")[1])
    print spatial_token
    with open("../ontology/frequency_sum","w") as fw1:
        fw1.write("ID|Token|AvgFreq\n")
        with open("../ontology/frequency","w") as fw2:
            count=0
            fw2.write("ID|Book|Token|Freq\n")
            for token in spatial_token:
                count+=1
                sum=float(percentage(text1.count(token),len(text1))) \
                    +float(percentage(text2.count(token),len(text2))) \
                    +float(percentage(text3.count(token),len(text3))) \
                    +float(percentage(text4.count(token),len(text4))) \
                    +float(percentage(text5.count(token),len(text5))) \
                    +float(percentage(text6.count(token),len(text6))) \
                    +float(percentage(text7.count(token),len(text7))) \
                    +float(percentage(text8.count(token),len(text8))) \
                    +float(percentage(text9.count(token),len(text9)))
                fw1.write("%d|%s|%.2f\n" % (count,token,sum/9))
                fw2.write("%d|%s|%s|%s\n" % (count,text1.name,token,percentage(text1.count(token),len(text1))))
                fw2.write("%d|%s|%s|%s\n" % (count,text2.name,token,percentage(text2.count(token),len(text2))))
                fw2.write("%d|%s|%s|%s\n" % (count,text3.name,token,percentage(text3.count(token),len(text3))))
                fw2.write("%d|%s|%s|%s\n" % (count,text4.name,token,percentage(text4.count(token),len(text4))))
                fw2.write("%d|%s|%s|%s\n" % (count,text5.name,token,percentage(text5.count(token),len(text5))))
                fw2.write("%d|%s|%s|%s\n" % (count,text6.name,token,percentage(text6.count(token),len(text6))))
                fw2.write("%d|%s|%s|%s\n" % (count,text7.name,token,percentage(text7.count(token),len(text7))))
                fw2.write("%d|%s|%s|%s\n" % (count,text8.name,token,percentage(text8.count(token),len(text8))))
                fw2.write("%d|%s|%s|%s\n" % (count,text9.name,token,percentage(text9.count(token),len(text9))))
                print count
                #raw_input("next")
    
    