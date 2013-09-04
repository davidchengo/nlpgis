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

# chunk parser
cp = RegexpParser('''
            V: {<VB>}
            NP: {<DT|PP\$>?<RB>?<JJ.*>*<NN|NNS>+}               # chunk determiner/possessive, adjectives and nouns
                {<NNP>+} # chunk sequences of proper nouns
            PP: {<IN><TO>?<JJ>?<DT>?<NN>?<IN>?}                 # Preposition
        ''')  # tag patterns 
        tree1=cp.parse(tagged)
        self.parse_tree_var.set(tree1)
        
        # spatial role labeling
        ''' coding:
        CONST_QUANT         quantity
        CONST_PROP          constraint property    
        SP_ENTITY              spatial object
        SP_CONST            spatial constrain
        '''
        cp = nlRegexpParser('''
            CONST_QUANT: {<DT>?<JJ>?<CD>}
            CONST_PROP: {<RB>?<JJ|JJR|JJS><^TO>|<CD><NN|NNS><RB>?}
            CONST: {<CONST_QUANT>?<CONST_PROP>?}
            SP_CLASS: {<NN|NNS>+}
            SP_ENTITY: {<NNP.*>+}
            SP_CONST: {<IN><TO>|<JJ.*><TO>|<IN>|<TO>|<IN><DT>?<NN><IN>}                                       # Preposition
        ''')
        tree2=cp.parse(tagged)
        self.spatial_role_var.set(tree2)
        
        # ontological role tagging
##        l=[]
##        self.traverse(tree2,l)
##        self.ontology_var.set("\n".join(l))

        if self.question_var.get().strip()=="restaurants next to Ohio State":
            s="""
restaurants: unspecified instances of the object type PLACE
next to: an instance of the spatial relationship type SPATIAL_PROXIMITY
Ohio State: an instance of the object type UNIVERITY
"""
        elif self.question_var.get().strip()=="very expensive restaurants next to Ohio State":
            s="""
very expensive: modifer of an object type instance
restaurants: unspecified instances of the object type PLACE
next to: an instance of the spatial relationship type SPATIAL_PROXIMITY
Ohio State: an instance of the object type UNIVERITY
"""
        else:
            s="""
restaurants: unspecified instances of the object type PLACE
next to: an instance of the spatial relationship type SPATIAL_PROXIMITY
campus: an unspecified instance of the object type UNIVERITY
"""
        self.ontology_var.set(s)
        self.update_view()
        print "done!"