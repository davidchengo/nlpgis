from nltk import *
from nltk.tag.stanford import POSTagger
PATH_TO_TAGGER=r'C:\\AptanaWorkspace\\Thesis\\src\\lib\\english-left3words-distsim.tagger'
PATH_TO_JAR=r'C:\\AptanaWorkspace\\Thesis\\src\\lib\\stanford-postagger.jar'
st = POSTagger(PATH_TO_TAGGER,PATH_TO_JAR)
s1="Where is the nearest city to Columbus?"
s2="Where is the nearest city to Ohio State University?"
tagged_question=st.tag(word_tokenize(s2))
s= corpus.treebank.tagged_sents()[22]
print s
print tagged_question
print ne_chunk(tagged_question)