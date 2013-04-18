'''
Created on Nov 27, 2012

@author: davidchen

http://nltk.googlecode.com/svn/trunk/doc/api/nltk.corpus.reader.wordnet.Synset-class.html
Create a Synset from a "<lemma>.<pos>.<number>" string where:
<lemma> is the word's morphological stem
<pos> is one of the module attributes ADJ, ADJ_SAT, ADV, NOUN or VERB
<number> is the sense number, counting from 0.

Synset attributes
-----------------
name - The canonical name of this synset, formed using the first lemma
    of this synset. Note that this may be different from the name
    passed to the constructor if that string used a different lemma to
    identify the synset.
pos - The synset's part of speech, matching one of the module level
    attributes ADJ, ADJ_SAT, ADV, NOUN or VERB.
lemmas - A list of the Lemma objects for this synset.
definition - The definition for this synset.
examples - A list of example strings for this synset.
offset - The offset in the WordNet dict file of this synset.
#lexname - The name of the lexicographer file containing this synset.

Synset methods
--------------
Synsets have the following methods for retrieving related Synsets.
They correspond to the names for the pointer symbols defined here:
    http://wordnet.princeton.edu/man/wninput.5WN.html#sect3
These methods all return lists of Synsets.

hypernyms
instance_hypernyms
hyponyms
instance_hyponyms
member_holonyms
substance_holonyms
part_holonyms
member_meronyms
substance_meronyms
part_meronyms
attributes
entailments
causes
also_sees
verb_groups
similar_tos

Additionally, Synsets support the following methods specific to the
hypernym relation:

root_hypernyms
common_hypernyms
lowest_common_hypernyms

Note that Synsets do not support the following relations because
these are defined by WordNet as lexical relations:

antonyms
derivationally_related_forms
pertainyms
'''
from nltk.corpus import wordnet as wn
from curses.ascii import SYN

if __name__ == '__main__':
    # 
    with open("../ontology/nationalfile_feature_class","r") as fr:
        #print fr.readline()
        for phrase in fr.readlines():
            # ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
            for syn in wn.synsets("near",'a'):
                #print phrase.strip()
                print syn.name,syn.pos
                print syn.lemma_names
                print syn.definition
                # In linguistics, a hyponym is a word or phrase whose semantic field[1] is included within that of another word, its hypernym
                print syn.examples
                exit()
                #print syn.examples
                print syn.hypernyms()
                ''''X' is a holonym of 'Y' if Ys are parts of Xs, 
                    or 'X' is a holonym of 'Y' if Ys are members of Xs.'''
                print syn.member_holonyms()
                print syn.root_hypernyms()
                print ",".join([a for syn in syn.lemmas[0].pertainyms() for a in syn.lemma_names])
                print syn.instance_hyponyms
            exit()