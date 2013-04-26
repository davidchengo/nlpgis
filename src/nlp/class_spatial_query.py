#!C:/ArcGISPython27/ArcGIS10.1/python.exe

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
#from class_bigram_chunker import *
from class_reference_tag_sequence import *
from class_data import *
from class_feature import *

class SpatialQuery:
    # declare static variables
    #print os.path.join(os.getcwd(), "src\\lib\\english-left3words-distsim.tagger"),\
    #    os.path.join(os.getcwd(), "src\\lib\\stanford-postagger.jar")
    PATH_TO_TAGGER = os.path.join(os.getcwd(), "src\\lib\\english-left3words-distsim.tagger")
    PATH_TO_JAR = os.path.join(os.getcwd(), "src\\lib\\stanford-postagger.jar")
    # stanford tagger
    stanford_tagger = POSTagger(PATH_TO_TAGGER, PATH_TO_JAR)
    conn = connect("dbname=Ohio user=postgres password=ohiostate")
    # lemmatizer from NLTK. 
    # >>> WordNetLemmatizer().lemmatize('having','v')
    # 'have'
    # >>> WordNetLemmatizer().lemmatize('has','v')
    # 'have'
    lmtzr = WordNetLemmatizer()        
    # a dictionary of tagged question templates used to compare with a new question
    # key: 0,1,2,3,4,5; value: [] of tagged sentence
    tagged_question_dict = {}
    cur = conn.cursor()
    sql="""SELECT tag,question_type_id FROM template"""
    cur.execute(sql)
    for row in cur.fetchall():
        tag=row[0]
        question_type_id=int(row[1])
        if not tagged_question_dict.has_key(question_type_id):
            tagged_question_dict[question_type_id] = []
        tagged_question_dict[question_type_id].append(tag)
        
    #set up
    question=None
    question_type_id=None
    question_type=None
    question_type_dict = {0:'unknown', 1:'location', 2:'proximity_entity', 3:'proximity_distance', 4:'proximity_buffer',5:'relative_location'}
    w_lst=None          # token list
    tagged_lst=None     # tagged sentence
    tag_lst=None        # tag list
    units=['mile', 'miles','kms', 'km', 'kilometers', 'kilometer','meters', 'ms', 'm','mi','mis']
    
    #parsing
    ref_tag_seq=None
    output=None
    input=None
    relation=None
    sql=None
    exit_status=False      # whenever found query is not possible, stop parsing
    dump_result=''
    
    # a matching sentence must have one of these features
    feature_set_dict={1:None,2:None,3:None,4:None,5:None}
    # distance question has a feature quorum of 1
    feature_set=FeatureSet(1)       # quorum = 1
    feature_lst=[]
    for key,lst in {wordnet.wordnet.NOUN:['location','where','coordinates'],
                    wordnet.wordnet.VERB:['located']}.iteritems():
        for a in lst:
            feature_lst.append(lmtzr.lemmatize(a, key))
    feature_set.add_feature(Feature(feature_lst,1))    # this feature votes 1
    feature_set_dict[1]=feature_set
    
    # proximity entity question has a feature quorum of 2
    feature_set=FeatureSet(2)       # quorum = 2
    feature_lst=[]
    for key,lst in {wordnet.wordnet.NOUN:['cities','villages','towns']}.iteritems():
        for a in lst:
            feature_lst.append(lmtzr.lemmatize(a, key))
    feature_set.add_feature(Feature(feature_lst,1))    # this feature votes 1
    
    feature_lst=[]
    for key,lst in {wordnet.wordnet.ADV:['nearest','closest']}.iteritems():
        for a in lst:
            feature_lst.append(lmtzr.lemmatize(a, key))
    feature_set.add_feature(Feature(feature_lst,1))    # this feature votes 1
    feature_set_dict[2]=feature_set
    
    # proximity distance question has a feature quorum of 2
    feature_set=FeatureSet(1)       # quorum =1
    feature_lst=[]
    for key,lst in {wordnet.wordnet.NOUN:['distance'],wordnet.wordnet.ADJ:['far']}.iteritems():
        for a in lst:
            feature_lst.append(lmtzr.lemmatize(a, key))
    feature_set.add_feature(Feature(feature_lst,1))    # this feature votes 1
    feature_set_dict[3]=feature_set
    
    # proximity buffer question has a feature quorum of 3
    feature_set=FeatureSet(3)       # quorum = 3
    feature_lst=[]
    for key,lst in {wordnet.wordnet.NOUN:['cities','villages','towns']}.iteritems():
        for a in lst:
            feature_lst.append(lmtzr.lemmatize(a, key))
    feature_set.add_feature(Feature(feature_lst,1))         # this feature votes 1
    
    feature_lst=[]
    for key,lst in {wordnet.wordnet.ADV:['within','outside','inside','beyond','in']}.iteritems():
        for a in lst:
            feature_lst.append(lmtzr.lemmatize(a, key))
    feature_set.add_feature(Feature(feature_lst,1))    # this feature votes 1
    
    feature_set.add_feature(Feature(units,1))    # this feature votes 1
    feature_set_dict[4]=feature_set

    # relative location question has a feature quorum of 2
    feature_set=FeatureSet(4)       # quorum = 2
    feature_lst=[]
    for key,lst in {wordnet.wordnet.NOUN:['where','location'],
                    wordnet.wordnet.VERB:['located']}.iteritems():
        for a in lst:
            feature_lst.append(lmtzr.lemmatize(a, key))
    feature_set.add_feature(Feature(feature_lst,1))    # this feature votes 1
    
    feature_lst=[]
    for key,lst in {wordnet.wordnet.NOUN:['relation'],
                    wordnet.wordnet.ADJ:['perspective','relative']}.iteritems():
        for a in lst:
            feature_lst.append(lmtzr.lemmatize(a, key))
    feature_set.add_feature(Feature(feature_lst,1))    # this feature votes 1
    
    feature_lst=[]
    for key,lst in {wordnet.wordnet.ADV:['to','of']}.iteritems():
        for a in lst:
            feature_lst.append(lmtzr.lemmatize(a, key))
    feature_set.add_feature(Feature(feature_lst,2))    # this feature votes 1
    
    feature_lst=[]
    for key,lst in {wordnet.wordnet.NOUN:['direction']}.iteritems():
        for a in lst:
            feature_lst.append(lmtzr.lemmatize(a, key))
    feature_set.add_feature(Feature(feature_lst,2))    # this feature votes 1
    feature_set_dict[5]=feature_set
    
    @staticmethod
    def init(): 
        for feature_set in SpatialQuery.feature_set_dict.itervalues():
            feature_set.reset()
        SpatialQuery.question=None
        SpatialQuery.question_type_id=None
        SpatialQuery.question_type=None
        SpatialQuery.w_lst=None          # token list
        SpatialQuery.tagged_lst=None     # tagged sentence
        SpatialQuery.tag_lst=None        # tag list
        #parsing
        SpatialQuery.ref_tag_seq=None
        SpatialQuery.output=None
        SpatialQuery.input=None
        SpatialQuery.relation=None
        SpatialQuery.sql=None
        SpatialQuery.exit_status=False
        SpatialQuery.dump_result=''
        
    @staticmethod
    def answer(s):  # s is the input raw sentence
        SpatialQuery.init()
        SpatialQuery.question = s       
        SpatialQuery.w_lst = word_tokenize(s)
        SpatialQuery.tagged_lst = SpatialQuery.stanford_tagger.tag(SpatialQuery.w_lst)
        SpatialQuery.tag_lst = [a[1] for a in SpatialQuery.tagged_lst]
        # get question type and the ref_tag_seq
        SpatialQuery.parse_question()
        SpatialQuery.dump_result+= '{:<30}{:<50}\n'.format("Tag sequence:",' '.join(SpatialQuery.tag_lst))
        SpatialQuery.dump_result+= '{:<30}{:<50}\n'.format("Reference tag sequence:",' '.join(SpatialQuery.ref_tag_seq.tag_lst))
        SpatialQuery.dump_result+= '{:<30}{:<50}\n'.format("LCS:",' '.join(SpatialQuery.ref_tag_seq.lcs))
        SpatialQuery.output = OutputData()  # an Data object\
        SpatialQuery.input = InputData()  # input can be a list
        SpatialQuery.relation = Relation()  # paired with input
        SpatialQuery.build_query()
        print SpatialQuery.dump_result
    @staticmethod
    def find_lcs(xs, ys):
        '''Return the longest subsequence common to xs and ys.
        Example
        >>> lcs("HUMAN", "CHIMPANZEE")
        ['H', 'M', 'A', 'N']
        '''
        def memoize(fn):
            '''Return a memoized version of the input function.
            The returned function caches the results of previous calls.
            Useful if a function call is expensive, and the function 
            is called repeatedly with the same arguments.
            '''
            cache = dict()
            def wrapped(*v):
                key = tuple(v)  # tuples are hashable, and can be used as dict keys
                if key not in cache:
                    cache[key] = fn(*v)
                return cache[key]
            return wrapped
        @memoize
        def lcs_(i, j):
            if i and j:
                xe, ye = xs[i - 1], ys[j - 1]
                if xe == ye:
                    return lcs_(i - 1, j - 1) + [xe]
                else:
                    return max(lcs_(i, j - 1), lcs_(i - 1, j), key=len)
            else:
                return []
        return lcs_(len(xs), len(ys))
    
    @staticmethod
    def parse_question():
        max_similarity = 0
        question_type_id = None
        o_lcs = None        # output lcs
        o_ref_tag_lst = None    # output ref tag list
        find_flg = False
        for key in sorted(SpatialQuery.tagged_question_dict.iterkeys()):    # 0,1,2,3..
            for ref_tag_seq in SpatialQuery.tagged_question_dict[key]:
                ref_tag_lst = ref_tag_seq.split()
                # current lcs
                lcs = SpatialQuery.find_lcs(ref_tag_lst, SpatialQuery.tag_lst)
                similary = (len(lcs) * 1.0 / len(ref_tag_lst) + len(lcs) * 1.0 / len(SpatialQuery.tag_lst)) / 2
                if similary == 1:               # assumption here is no same tag sequence among different categories 
                    max_similarity = similary
                    question_type_id = key
                    o_lcs = lcs
                    o_ref_tag_lst = ref_tag_lst
                    find_flg = True
                    break
                elif similary > max_similarity:
                    max_similarity = similary
                    question_type_id = key
                    o_lcs = lcs
                    o_ref_tag_lst = ref_tag_lst      
            if find_flg: 
                break
        SpatialQuery.question_type_id=question_type_id
        SpatialQuery.question_type=SpatialQuery.question_type_dict[SpatialQuery.question_type_id]
        # subsequent parsing is based on ref tag seq
        SpatialQuery.ref_tag_seq=ReferenceTagSequence(max_similarity, o_lcs, o_ref_tag_lst, question_type_id)
        SpatialQuery.dump_result+= "\nTagged sentence: "+' '.join([ w+'/'+t for w,t in SpatialQuery.tagged_lst])+'\n'
        if SpatialQuery.ref_tag_seq.similarity == 1:
            SpatialQuery.dump_result+= "Exact same template found. Highest similarity: 1.00. Question type: %s.\n" % (SpatialQuery.question_type)
        else:
            SpatialQuery.dump_result+= "No exact same template found. Highest similarity: %.2f. Question type: %s.\n" % \
            (SpatialQuery.ref_tag_seq.similarity, SpatialQuery.question_type)
    
    @staticmethod   
    def build_query():
        if SpatialQuery.question_type_id== 1:
            SpatialQuery.build_location_query()
        elif SpatialQuery.question_type_id == 2:
            SpatialQuery.build_proximity_entity_query()
        elif SpatialQuery.question_type_id == 3:
            SpatialQuery.build_proximity_distance_query()
        elif SpatialQuery.question_type_id == 4:
            SpatialQuery.build_proximity_buffer_query()
        elif SpatialQuery.question_type_id == 5:
            SpatialQuery.build_relative_location_query()    
    
    @staticmethod
    def check_query():
        SpatialQuery.dump_result+= "\nMatching template features:\n"
        tmp_dump_lst=[]
        for word in SpatialQuery.w_lst:
            token=SpatialQuery.lmtzr.lemmatize(word).lower()
            flg=SpatialQuery.feature_set_dict[SpatialQuery.question_type_id].isFeatureQuorumMet(token,tmp_dump_lst)
            SpatialQuery.dump_result+='\n'.join(tmp_dump_lst)
            tmp_dump_lst=[]
            if flg==True:
                return True
        return False
            
    @staticmethod
    def build_location_query():
        # tag_lst=self.ref_tag_seq.tag_lst
        # location question, parameter NN|NNS -> type, NNP|NNPS -> value, no constraint
        if SpatialQuery.check_query():      # make sure it is a location question
            SpatialQuery.dump_result+= "Location question features match! Query can be built.\n"
            # resolve input; no need to resolve output and relation
            SpatialQuery.resolve_input()
            SpatialQuery.print_sql_components()
            SpatialQuery.sql = """SELECT name, ASTEXT(t.geom) As loc
FROM ohio_place As t
WHERE t.name in (%s)
""" % ("'" + "','".join(SpatialQuery.input.value_lst) + "'")
            SpatialQuery.dump_result+= "\nSQL:\n%s" % SpatialQuery.sql
            SpatialQuery.querydb()
        else:
            SpatialQuery.dump_result+= "\nUnknown location question. Query can't be built"
            
    @staticmethod    
    def build_proximity_entity_query():
        if SpatialQuery.check_query():      # check if it is a proximity entity question
            # resolve input
            SpatialQuery.resolve_input()
            if SpatialQuery.exit_status==True:
                return
            # resolve output
            # output: type, quantity and quality constraints
            SpatialQuery.resolve_output()
            if SpatialQuery.exit_status==True:
                return
            for w,t in SpatialQuery.tagged_lst:
                if w in ['closest','nearest']:
                    SpatialQuery.output.order='ASC'
                    break
                elif w in ['farthest','furthest']:
                    SpatialQuery.output.order='DESC'
                    break
            SpatialQuery.print_sql_components()
            SpatialQuery.sql = """SELECT t_out.name As name,ST_Distance(ST_Transform(t_in.geom,2163),ST_Transform(t_out.geom,2163)) as dist, t_out.type As type
FROM ohio_place As t_in, ohio_place As t_out   
WHERE t_in.name IN (%s) AND t_in.id <> t_out.id %s""" % ("'" + "','".join(SpatialQuery.input.value_lst) + "'", 
            SpatialQuery.output.qualityconstraint2sql('t_out'))

            SpatialQuery.sql+="""
ORDER BY dist %s
LIMIT %d
""" % (     SpatialQuery.output.order,
            SpatialQuery.output.count)

            SpatialQuery.dump_result+= "\nSQL:\n%s" % SpatialQuery.sql
            SpatialQuery.querydb()
        else:
            SpatialQuery.dump_result+= "\nUnknown proximity entity question. Query can't be built"
    
    @staticmethod
    def build_proximity_distance_query():
        if SpatialQuery.check_query():
            SpatialQuery.dump_result+= "Distance question features match! Query can be built."
            # resolve input; no need to resolve output and relation
            SpatialQuery.resolve_input()    # only accept two inputs for distance question
            #SpatialQuery.resolve_relation()   
            SpatialQuery.print_sql_components()
            SpatialQuery.sql = """SELECT t_in1.name As from_name, t_in2.name As to_name, 
ST_Distance(ST_Transform(t_in1.geom,2163),ST_Transform(t_in2.geom,2163)) as dist
FROM ohio_place As t_in1, ohio_place As t_in2   
WHERE t_in1.name ='%s' and t_in2.name ='%s' 
""" % (SpatialQuery.input.value_lst[0], SpatialQuery.input.value_lst[1])
            print "\nSQL:\n%s" % SpatialQuery.sql
            SpatialQuery.querydb()
        else:
            print "\nUnknown proximity distance question. Query can't be built."
            
    @staticmethod
    def build_proximity_buffer_query():
        if SpatialQuery.check_query():
            # resolve input
            SpatialQuery.resolve_input()
            if SpatialQuery.exit_status==True:
                return
            # resolve output
            # output: type, quantity and quality constraints
            SpatialQuery.resolve_output()
            if SpatialQuery.exit_status==True:
                return
            for w,t in SpatialQuery.tagged_lst:
                if w in ['closest','nearest']:
                    SpatialQuery.output.order='ASC'
                    break
                elif w in ['farthest','furthest']:
                    SpatialQuery.output.order='DESC'
                    break
            
            SpatialQuery.sql = """SELECT distinct t_out.name As out_name
FROM ohio_place As t_out, ohio_place As t_in  
WHERE %s""" %(SpatialQuery.input.bufferconstraint2sql())
            if SpatialQuery.output.count>1:
                SpatialQuery.sql += "LIMIT %d" % SpatialQuery.output.count
            SpatialQuery.dump_result+= "\nSQL:\n%s" % SpatialQuery.sql
            SpatialQuery.querydb()
        else:
            SpatialQuery.dump_result+= "\nUnknown proximity buffer question. Query can't be built."
    
    @staticmethod    
    def print_sql_components():
        SpatialQuery.dump_result+= "\nSQL component analysis:\n"
        SpatialQuery.dump_result+= SpatialQuery.input.to_str()+'\n'
        try:
            SpatialQuery.dump_result+= SpatialQuery.input.constraint.to_str()+'\n'
        except Exception as e:
            pass
        SpatialQuery.dump_result+= SpatialQuery.output.to_str()+'\n'
        try:
            SpatialQuery.dump_result+= SpatialQuery.output.constraint.to_str()+'\n'
        except Exception as e:
            pass
        SpatialQuery.dump_result+= SpatialQuery.relation.to_str()+'\n'
        try:
            SpatialQuery.dump_result+= SpatialQuery.relation.constraint.to_str()+'\n'
        except Exception as e:
            pass
    
    @staticmethod
    def find_numbers(tagged):
        # 21, twenty one, one hundred and one
        cp = RegexpParser('''
            numbers: {<CD>*<CC>*<CD>+}        
        ''')  # tag patterns 
        tree = cp.parse(tagged)
        digit_lst = []
        digit_dict = {'one':'1', 'two':'2', 'three':'3', 'four':'4', 'five':'5', 'six':'6', 'seven':'7',
'eight':'8', 'nine':'9', 'ten':'10', 'eleven':'11', 'twelve':'12', 'thirteen':'13', 'fourteen':'14',
'fifteen':'15', 'sixteen':'16', 'seventeen':'17', 'eighteen':'18', 'nineteen':'19', 'twenty':'2',
'thirty':'3', 'fourty':'4', 'fifty':'5', 'sixty':'6', 'seventy':'7', 'eighty':'8', 'ninety':'9',
'hundred':'00', 'thousand':'000'}
        for a in tree:
            try:
                if a.node:
                    
                    word_lst = [w_t[0].split('-') for w_t in a]
                    word_lst = [item for sublist in word_lst[:] for item in sublist]
                    for word in word_lst:
                        word = word.lower()
                        if digit_dict.has_key(word):
                            digit_lst.append(digit_dict[word])
                        elif word.isdigit():
                            digit_lst.append(word)
            except Exception as e:
                #print str(e)
                pass
        if len(digit_lst) > 0:
            return int(''.join(digit_lst))
        else:
            # default return 1 output
            return 1
    
    @staticmethod
    def resolve_input():
        # within 10 miles of Columbus and 20 miles of Dayton
        # within 10 miles of Columbus and Dayton
        # within 10 miles of Columbus
        
        cp = RegexpParser('''
            input:  {<IN><CD>*<CC>*<CD>+<NN.*>+<IN>*<TO>*<NNP.*>+<CC><CD>*<CC>*<CD>+<NN.*>+<IN>*<TO>*<NNP.*>+}
                    {<IN><CD>*<CC>*<CD>+<NN.*>+<IN>*<TO>*<NNP.*>+<CC><NNP.*>+}
                    {<IN><CD>*<CC>*<CD>+<NN.*>+<IN>*<TO>*<NNP.*>+}    
                    {<NNP.*>+}        
        ''')  # tag patterns 
        tree = cp.parse(SpatialQuery.tagged_lst)
        SpatialQuery.dump_result+= "\nInput chunks:\n"+tree.pprint()+"\n"
        # (S where/WRB are/VBP (place Columbus/NNP) and/CC (place Dayton/NNP))
        for a in tree:
            try:
                if a.node:          # a -> (place Columbus/NNP), (place Arlington/NNP Heights/NNP)
                    cp_place_name = RegexpParser('''
                            place_name:  {<NNP.*>+}
                    ''')  # tag patterns 
                    tree_place_name=cp_place_name.parse(a)
                    for b in tree_place_name:
                        try:
                            if b.node:
                                SpatialQuery.input.value_lst.append(' '.join([w for w,t in b]));
                        except Exception as e:
                            #print str(e)
                            pass
                    # parse input constraints in the chunk
                    if a[0][1] in ['IN']:
                        spatial_term=a[0][0].lower()
                        if spatial_term in ['within','in','inside']:
                            category='buffer'
                            SpatialQuery.relation.category='buffer'
                        cp_num = RegexpParser('''
                                input:  {<CD>*<CC>*<CD>+<NN.*>} 
                        ''')  # tag patterns 
                        tree_num=cp_num.parse(a)
                        for b in tree_num:
                            try:
                                if b.node:
                                    # find unit
                                    for w,t in b:
                                        if t in ['NN','NNS'] and w.lower() in SpatialQuery.units:
                                            # only one input value in this chunk
                                            unit=w
                                    # find value
                                    value=SpatialQuery.find_numbers(b)
                                    SpatialQuery.input.constraint_lst.append(
                                            QuantityConstraint(value,category,unit,"ST_WITHIN"))
                            except Exception as e:
                                #print str(e)
                                pass
            except Exception as e:
                #print str(e)
                pass
        
            
    @staticmethod
    def resolve_output():
        # e.g. three nearest major cities
        cp = RegexpParser('''
            output: 
                {<CD>*<CC>*<CD>*<IN>*<JJ.*>*<NN.*>+(<IN>|<VBP>)}        
        ''')  # tag patterns 
        tree = cp.parse(SpatialQuery.tagged_lst)
        SpatialQuery.dump_result+= "\nOutput chunks:\n"+ tree.pprint()+'\n'
        for a in tree:
            try:
                if a.node:      # a is the noun phrase including all information about the output
                    last_noun=a[len(a)-2][0].lower() 
                    if last_noun in SpatialQuery.units:
                        continue
                    # parse numbers
                    # a number in the output is not necessarily the output count
                    # e.g. 3 nearest major cities within
                    # parse output constraint, spatial relation
                    # not all nouns are output types, can be constraints.
                    # e.g. a corn city, a football player
                    # if the noun is a unit, skip
                    last_noun_lemma=SpatialQuery.lmtzr.lemmatize(last_noun)
                    if last_noun_lemma in ['city','village','town']:
                        SpatialQuery.output.category=last_noun_lemma
                        SpatialQuery.output.count=SpatialQuery.find_numbers(a)
                    else:
                        SpatialQuery.dump_result+= "\nUnknown output category: %s. Exit.\n" %  last_noun_lemma
                        SpatialQuery.exit_status=True
                        return
                    # parse property constraints of the output. Search from the beginning to len-2. Process only JJ.* and Nouns
                    for i in xrange(0,len(a)-2):
                        w=a[i][0].lower()
                        t=a[i][1]
                        if t in ['NN','NNS','JJ','JJS','JJR','IN']:
                            if w in ['nearest','closest']:
                                SpatialQuery.output.order="ASC"
                            elif w in ['farthest','furthest']:
                                SpatialQuery.output.order="DESC"
                            if w in ['big', 'major','large','principal','small','secondary']:
                                SpatialQuery.output.constraint_lst.append(QualityConstraint(w,'population'))                                                  
            except Exception as e:
                #print str(e)
                pass
            
    @staticmethod
    def resolve_relation():
        lst=[]
        # from Grandview Heights to Dayton
        # between Grandview Heights and Dayton
        # from Grandview Heights 
        # clauses of the following grammar are executed in order
        cp = RegexpParser('''
            PP: {<IN><NNP.*>+<CC><NNP.*>+}   
                {<IN><NNP.*>+<TO><NNP.*>+} 
                {<IN><NNP.*>+} 
        ''')  # tag patterns 
        tree = cp.parse(SpatialQuery.tagged_lst)
        for a in tree:
            try:
                if a.node:          # a -> (place Columbus/NNP), (place Arlington/NNP Heights/NNP)
                    for w,t in a:
                        if t in ['IN','TO']:
                            lst.append(w)
            except:
                pass
        SpatialQuery.relation.type=' '.join(lst)

    
    @staticmethod
    def querydb():
        cur = SpatialQuery.conn.cursor()
        try:
            cur.execute(SpatialQuery.sql)    
            SpatialQuery.dump_result+= "\nSQL succeed!\n"
            rows = cur.fetchall()
            if len(rows)==0:
                SpatialQuery.dump_result+= "But no results returned."
                return
            SpatialQuery.dump_result+= '\nQuestion:\n%s\n' % SpatialQuery.question
            SpatialQuery.dump_result+= "\nAnswer:\n----------------------------------------\n"
            # format answers based on question type
            if SpatialQuery.question_type == 'location':
                SpatialQuery.dump_result+= '{:<20}{:<30}\n'.format("Name","Location")
                for row in rows:
                    SpatialQuery.dump_result+= '{:<20}{:<30}\n'.format(row[0], row[1])
                    
            if SpatialQuery.question_type == 'proximity_entity':
                SpatialQuery.dump_result+= '{:<20}{:<20}{:<30}\n'.format("Name","Distance(mile)","Type")
                for row in rows:
                    SpatialQuery.dump_result+= '{:<20}{:<20.2f}{:<30}\n'.format(row[0], float(row[1])/1609.34, row[2])
                    
            if SpatialQuery.question_type == 'proximity_distance':
                SpatialQuery.dump_result+= '{:<20}{:<20}{:<20}\n'.format("From_Name","To_Name","Distance(mile)")
                for row in rows:
                    SpatialQuery.dump_result+= '{:<20}{:<20}{:<20.2f}\n'.format(row[0], row[1], float(row[2])/1609.34)
                    
            if SpatialQuery.question_type == 'proximity_buffer':
                SpatialQuery.dump_result+= "Name\n"
                for row in rows:
                    SpatialQuery.dump_result+= "%s\n" % (row[0])
            SpatialQuery.dump_result+= "----------------------------------------"
        except Exception, e:
            SpatialQuery.dump_result+= str(e)
            SpatialQuery.dump_result+= "SQL not succeed!"
            SpatialQuery.conn.rollback()
