#!C:/ArcGISPython27/ArcGIS10.1/python.exe

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
    cgitb.enable()
    s_lst = ["distance between Columbus and Dayton",
           "distance Columbus Dayton"]
    for s in s_lst:
        print s
        sq = SpatialQuery(s)
        result = sq.query()
        print '----------------------------------------'
