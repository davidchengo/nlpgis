'''
Created on Nov 27, 2012

@author: davidchen
'''
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
from class_spatial_query import *
import cgitb

if __name__ == '__main__':
    s_lst = ["What is Columbus's location"]
    for s in s_lst:
        sq = SpatialQuery(s)
        sq.query()
        print '----------------------------------------'
