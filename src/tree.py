'''
Created on Nov 27, 2012

@author: davidchen
'''
from nltk.tree import *
from nltk.draw import tree

if __name__ == '__main__':
    print Tree(1, [2, 3, 4])
    s = Tree('S', [Tree('NP', ['I']),
           Tree('VP', [Tree('V', ['saw']),
               Tree('NP', ['him'])])])
    print s
    s.draw()