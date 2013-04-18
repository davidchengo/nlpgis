from Tkinter import *
from tkFont import *
from nltk import *
from nltk.tag.stanford import POSTagger
PATH_TO_TAGGER=r'C:\\AptanaWorkspace\\Thesis\\src\\lib\\english-left3words-distsim.tagger'
PATH_TO_JAR=r'C:\\AptanaWorkspace\\Thesis\\src\\lib\\stanford-postagger.jar'
st = POSTagger(PATH_TO_TAGGER,PATH_TO_JAR)
s="Where is the nearest restaurant to the campus?"
tagged_question=st.tag(word_tokenize(s))
print "POS tagging:",' '.join([ w+'/'+t for w,t in tagged_question])
