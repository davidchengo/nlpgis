#!C:/ArcGISPython27/ArcGIS10.1/python.exe

from nltk import *
from nltk.corpus import conll2000
from nltk.tag.stanford import POSTagger
import nltk.chunk
import glob
import os, time
import csv
import codecs
from psycopg2 import connect 
import pprint
from nltk.stem.wordnet import WordNetLemmatizer

class BigramChunker(nltk.ChunkParserI):
    def __init__(self, train_sents): 
        train_data = [[(t, c) for w, t, c in nltk.chunk.tree2conlltags(sent)]
                      for sent in train_sents]
#        with open('conll2000_chunked_sents','w') as fw:
#            for sent in train_data[:10]:
#                print sent
#                for t,c in sent:
#                    fw.write("%s\t%s\n"%(t,c))

        self.tagger = nltk.BigramTagger(train_data) 

    def parse(self, sentence): 
        pos_tags = [pos for (word, pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        conlltags = [(word, pos, chunktag) for ((word, pos), chunktag)
                     in zip(sentence, chunktags)]
        tree = nltk.chunk.util.conlltags2tree(conlltags)
        return tree
