import os
from nltk import *
from nltk.tag.stanford import POSTagger
from nltk.stem.wordnet import WordNetLemmatizer
PATH_TO_TAGGER = os.path.join(os.getcwd(), "lib\\wsj-0-18-bidirectional-nodistsim.tagger")
PATH_TO_JAR = os.path.join(os.getcwd(), "lib\\stanford-postagger.jar")
print pos_tag("the sea touches me".split())
stanford_tagger = POSTagger(PATH_TO_TAGGER,PATH_TO_JAR)
print stanford_tagger.tag(word_tokenize("which ocean touches the state of California ?"))