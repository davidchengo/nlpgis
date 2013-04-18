'''
Created on Nov 1, 2012

@author: davidchen
'''
from nltk import *

if __name__ == '__main__':
  text = word_tokenize("the running kids at the end of the row")
  tagged_text = pos_tag(text)
  print tagged_text