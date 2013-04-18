'''
Created on Nov 27, 2012

@author: davidchen
'''
# Automatic language understanding 
# word sense disambiguation
# Pronoun Resolution:
    #anaphora resolution identifying what a pronoun or noun phrase refers to
    #semantic role labeling identifying how a noun phrase relates to the verb (as agent,patient, instrument, and so on).
# 

from nltk import *
from nltk.corpus import gutenberg
if __name__ == '__main__':
    '''In a sentence containing the phrase: he served the dish, you can detect that both serve
and dish are being used with their food meanings. Its unlikely that the topic of discussion
shifted from sports to crockery in the space of three words. This would force you
to invent bizarre images, like a tennis pro taking out his frustrations on a china tea-set
laid out beside the court. In other words, we automatically disambiguate words using
context, exploiting the simple fact that nearby words have closely related meanings.'''
    
    '''As another example of this contextual effect, consider the word by, which has several
meanings, for example, the book by Chesterton (agentive Chesterton was the author
of the book); the cup by the stove (locative the stove is where the cup is); and submit
by Friday (temporal Friday is the time of the submitting).
['austen-emma.txt', 'austen-persuasion.txt', 'austen-sense.txt', 'bible-kjv.txt', 
'blake-poems.txt', 'bryant-stories.txt', 'burgess-busterbrown.txt', 'carroll-alice.txt', 
'chesterton-ball.txt', 'chesterton-brown.txt', 'chesterton-thursday.txt', 'edgeworth-parents.txt', 
'melville-moby_dick.txt', 'milton-paradise.txt', 'shakespeare-caesar.txt', 'shakespeare-hamlet.txt', 
'shakespeare-macbeth.txt', 'whitman-leaves.txt']
'''
    #print corpus.gutenberg.fileids()
#    text=Text(gutenberg.words('bible-kjv.txt'))
#    print text.concordance("in")        # this helps find sample sentence segments with specified key words
    
    for fileid in gutenberg.fileids():
        num_chars = len(gutenberg.raw(fileid))
        num_words = len(gutenberg.words(fileid))
        # The sents() function divides the text up into its sentences, where each sentence is a list of words
        # this can be used to find sample sentence
        num_sents = len(gutenberg.sents(fileid))    
        num_vocab = len(set([w.lower() for w in gutenberg.words(fileid)]))
        print int(num_chars/num_words), int(num_words/num_sents), int(num_words/num_vocab),fileid