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
from class_bigram_chunker import *
from class_reference_tag_sequence import *
from class_data import *

class SpatialQuery:
    PATH_TO_TAGGER = r'C:\\AptanaWorkspace\\Thesis\\src\\lib\\english-left3words-distsim.tagger'
    PATH_TO_JAR = r'C:\\AptanaWorkspace\\Thesis\\src\\lib\\stanford-postagger.jar'
    stanford_tagger = POSTagger(PATH_TO_TAGGER, PATH_TO_JAR)
    conll_sents = conll2000.chunked_sents()
    bigram_chunker = BigramChunker(conll_sents[:2000])
    
    conn = connect("dbname=Ohio user=postgres password=ohiostate")
    lmtzr = WordNetLemmatizer()
    tagged_question_dict = {}
    count = 0
    with open('question_tagged_data.txt', 'r') as fr:
        while(1):
            line = fr.readline()
            line = line.strip()
            if line == '':
                break
            if line[0] <> '#':
                tagged_question_dict[count].append(line)
            else:
                count += 1
                tagged_question_dict[count] = []
#    print tagged_question_dict
    
    def __init__(self, s):
        # initialize class variables tagger and chunker
        # training sents at least 2000
        self.question = s       
        self.w_lst = word_tokenize(s)
        self.tagged_lst = SpatialQuery.stanford_tagger.tag(self.w_lst)
        self.tag_lst = [a[1] for a in self.tagged_lst]
        self.question_type, self.ref_tag_seq = self.parse_question_type(SpatialQuery.tagged_question_dict, self.tag_lst)
        print self.ref_tag_seq.tag_lst, self.ref_tag_seq.lcs, self.ref_tag_seq.similarity
        self.output = OutputData()  # an Data object\
        self.input = InputData()  # input can be a list
        self.relation = Relation()  # paired with input
        self.sql = None
        self.build_query()
#            self.ck_tree=SpatialQuery.bigram_chunker.parse(self.tagged_lst) # chunk tree
#            self.print_chunk_result(self.ck_tree)
        


    
    def find_lcs(self, xs, ys):
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
    
        
    question_type_dict = {0:'unknown', 1:'location', 2:'proximity_entity', 3:'proximity_distance', 4:'proximity_buffer'}
    def parse_question_type(self, tagged_question_dict, tag_lst):
        max_similarity = 0
        question_type_id = None
        o_lcs = None
        o_ref_tag_lst = None
        find_flg = False
        for key in sorted(tagged_question_dict.iterkeys()):
#            if self.w_lst[0] not in ['how','what'] and key==3:      # first word heuristic
#                # can't be distanc question
#                continue
            if 'distance' in self.w_lst:
                if key <> 3:
                    continue
            for ref_tag_seq in tagged_question_dict[key]:
                ref_tag_lst = ref_tag_seq.split()
                lcs = self.find_lcs(ref_tag_lst, tag_lst)
                similary = (len(lcs) * 1.0 / len(ref_tag_lst) + len(lcs) * 1.0 / len(tag_lst)) / 2
                if similary == 1:
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
        return SpatialQuery.question_type_dict[question_type_id], \
                ReferenceTagSequence(max_similarity, o_lcs, o_ref_tag_lst, question_type_id)
    
    def build_location_query(self):
        # tag_lst=self.ref_tag_seq.tag_lst
        # location question, parameter NN|NNS -> type, NNP|NNPS -> value, no constraint
        if self.question.lower().find('where') <> -1 or self.question.lower().find('location') <> -1 or self.question.lower().find('located') <> -1:   
            self.output.set_type('location')
        else:
            print 'Unkown question'
            
        for i in xrange(len(self.tag_lst)):  # go through all tags
            w = self.w_lst[i]
            t = self.tag_lst[i]
            if t in ['NNP', 'NNPS']:
                self.input.resolve_type(w)
                self.input.add_value(w)
                
        self.print_gis_components()
        self.sql = """SELECT name, ASTEXT(t.geom) As loc
FROM ohio_place As t
WHERE t.name in (%s)
""" % ("'" + "','".join(self.input.value_lst) + "'")
        
        
    def build_proximity_entity_query(self):
        self.output.set_count(self.find_numbers(self.tagged_lst))
        for i in xrange(len(self.tag_lst)):  # go through all tags
            w = self.w_lst[i]
            t = self.tag_lst[i]
            if t in ['NN', 'NNS']:
                lemma = self.lmtzr.lemmatize(w, 'n')
                # print lemma
                if lemma in ['city', 'town', 'village']:
                    self.output.set_type(lemma)
                else:
                    print 'Unkown output type', w
                    break
            elif t in ['NNP', 'NNPS']:  # only one input value
                self.input.resolve_type(w)
                self.input.add_value(w)
            elif w in ['nearest', 'closest']:
                lemma = self.lmtzr.lemmatize(w, 'n')
                print lemma
                self.relation.resolve_type(lemma)
        self.print_gis_components()
        self.sql = """SELECT t_out.name As name, ASTEXT(t_out.geom) As location, 
ST_Distance(ST_Transform(t_in.geom,2163),ST_Transform(t_out.geom,2163)) as dist
FROM ohio_place As t_in, ohio_place As t_out   
WHERE t_in.name IN (%s) and t_in.id <> t_out.id 
ORDER BY dist %s
LIMIT %d
""" % ("'" + "','".join(self.input.value_lst) + "'",
       self.relation.order,
       self.output.count)
    
    
    def build_proximity_distance_query(self):
        if self.question.lower().find('how far') <> -1 or self.question.lower().find('distance') <> -1:
            self.output.set_type('distance')
            self.relation.set_type('distance')  
            for i in xrange(len(self.tag_lst)):  # go through all tags
                w = self.w_lst[i]
                t = self.tag_lst[i]
                if t in ['NNP', 'NNPS']:  # only one input value
                    self.input.resolve_type(w)
                    self.input.add_value(w)
        self.sql = """SELECT t_in1.name As from_name, ASTEXT(t_in1.geom) As from_loc,t_in2.name As to_name, ASTEXT(t_in2.geom) As to_loc, 
ST_Distance(ST_Transform(t_in1.geom,2163),ST_Transform(t_in2.geom,2163)) as dist
FROM ohio_place As t_in1, ohio_place As t_in2   
WHERE t_in1.name ='%s' and t_in2.name ='%s' 
""" % (self.input.value_lst[0], self.input.value_lst[1])


    def build_proximity_buffer_query(self):
        if self.question.lower().find('within') <> -1 or self.question.lower().find('inside') <> -1:
            self.relation.set_type('buffer')
            self.relation.constraint = QuantityConstraint()
            self.relation.constraint.set_type('distance')  # type correspond to db field
            value = self.find_numbers(self.tagged_lst)
            unit = ''
            for i in xrange(1, len(self.tag_lst)):
                if self.tag_lst[i] in ['NN', 'NNS'] and self.tag_lst[i - 1] == 'CD':
                    self.relation.constraint.add_unit(self.w_lst[i])
                    break
            self.relation.constraint.add_operator("<")
            self.relation.constraint.add_value(value)
            
        output_found = False
        for i in xrange(len(self.tag_lst)):
            w = self.w_lst[i]
            t = self.tag_lst[i]
            if output_found == False and t in ['NN', 'NNS']:
                lemma = self.lmtzr.lemmatize(w, 'n')
                print lemma
                if lemma in ['city', 'town', 'village']:
                    self.output.set_type(lemma)
                else:
                    print 'Unknown output type', w
                    break
                output_found = True
            if t in ['NNP', 'NNPS']:  # only one input value
                self.input.resolve_type(w)
                self.input.add_value(w)    
        
        self.sql = """SELECT t_out.name As out_name,ST_Distance(ST_Transform(t_out.geom,2163),ST_Transform(t_in.geom,2163)) as dist
FROM ohio_place As t_out, ohio_place As t_in  
WHERE t_in.name IN (%s) AND t_out.name NOT IN (%s)""" % ("'" + "','".join(self.input.value_lst) + "'", "'" + "','".join(self.input.value_lst) + "'")
        for i in xrange(len(self.relation.constraint.value_lst)):
            operator = self.relation.constraint.operator_lst[i]
            unit = self.relation.constraint.unit_lst[i]
            value = self.relation.constraint.value_lst[i]
            if unit.lower() in ['mile', 'miles']:
                value = value * 1609.34
            elif unit.lower() in ['kms', 'km', 'kilometers', 'kilometer']:
                value = value * 1000
            elif unit.lower() not in ['meters', 'ms', 'm']:
                print 'Unknown unit: ', unit
                
            if operator == '<':
                self.sql += """ AND ST_DWithin(ST_Transform(t_out.geom,2163), ST_Transform(t_in.geom,2163), %f) 
""" % value
            if operator == '>':
                self.sql += """ AND NOT ST_DWithin(ST_Transform(t_out.geom,2163), ST_Transform(t_in.geom,2163), %f) 
""" % value
        self.sql += "ORDER BY dist"
        print self.sql
        
    def build_query(self):
        print self.tagged_lst
        if self.ref_tag_seq.similarity == 1:
            print "Exact same question pattern found.\n"
        else:
            print "No exactly same question pattern found. Highest similarity: %.2f. Question type: %s.\n" % \
            (self.ref_tag_seq.similarity, self.question_type)
        if self.ref_tag_seq.question_category_id == 1:
            self.build_location_query()
        elif self.ref_tag_seq.question_category_id == 2:
            self.build_proximity_entity_query()
        elif self.ref_tag_seq.question_category_id == 3:
            self.build_proximity_distance_query()
        elif self.ref_tag_seq.question_category_id == 4:
            self.build_proximity_buffer_query()
            
        # build sql
        return
        
    def print_gis_components(self):
        try:
            print self.input.to_str()
        except Exception as e:
            print e
        try:
            print "Input constraint: ", self.input.constraint.to_str()
        except Exception as e:
            print 'No constraint on input data.'
            
        try:
            print self.output.to_str()
        except Exception as e:
            print e
        try:
            print "Output constraint: ", self.output.constraint.to_str()
        except Exception as e:
            print 'No constraint on output data.'
        
        try:
            print "Relation type: ", self.relation.to_str()
        except Exception as e:
            print 'No relation.'
        try:
            print "Relation constraint: ", self.relation.constraint.to_str()
        except Exception as e:
            print 'No constraint on relation.'
        
    def print_chunk_result(self, ck_tree):
        print "\nIntermediate results.."
        print "\nChunking result:"
        print ck_tree
        print '\nUseful chunks:'
        for a in ck_tree:
            try:
                if a.node in ['VP', 'NP', 'PP']:
                    # The node value is stored using the node attribute:
                    print a
            except:
                # not a chunk
                pass
    
    def find_numbers(self, tagged_lst):
        cp = RegexpParser('''
            numbers: {<CD>*<CC>*<CD>+}
        ''')  # tag patterns 
        tree = cp.parse(tagged_lst)
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
            except:
                pass
        if len(digit_lst) > 0:
            return int(''.join(digit_lst))
        else:
            return 1
        
    def find_name(self, lst, s):
        ne_tree = ne_chunk(lst)
        # print ne_tree
        for a in ne_tree:
            try:
                if a.node:
                    phrase = ' '.join([w_t[0] for w_t in a])
                    self.value_dict[s]['name'].append(phrase)  # Columbus
            except:
                pass
    
    def find_category(self, lst, s):
        cp = RegexpParser('''
            category: {<NN|NNS>+}
            }<W.*|DT|CD|JJ.*>+{
        ''')  # tag patterns 
        tree = cp.parse(lst)
        for a in tree:
            try:
                if a.node:
                    phrase = ' '.join([w_t[0] for w_t in a])
                    phrase_lemma = self.lmtzr.lemmatize(phrase, 'n')
                    if phrase_lemma not in self.value_dict[s]['category']:
                        self.value_dict[s]['category'].append(phrase_lemma)  # Columbus
                    self.relation_dict[s] += a[:]
                    # print phrase
            except:
                pass
        if s == 'output' and self.relation_type <> '':
            if self.relation_type == 'proximity':
                category1_keyword_lst = ['city', 'village', 'town', 'place']
                category2_keyword_lst = ['distance']
                if self.found_string(category1_keyword_lst, self.value_dict[s]['category']):  # return city
                    self.question_type = 'proximity_entity'
                elif self.found_string(category2_keyword_lst, self.value_dict[s]['category']): 
                    self.question_type = 'proximity_distance'
            print '\nQuestion type:%s\n' % self.question_type
    
    def found_string(self, substr_lst, str_lst):
        """Return true if s is a substring of one of the strings in the list"""
        flg = False
        for s1 in substr_lst:
            for s2 in str_lst:
                flg = ' ' + s1 + ' ' in ' ' + s2 + ' '
                if flg == True:
                    return flg
        return flg
    
    def query(self):
        cur = self.conn.cursor()
        try:
            cur.execute(self.sql)    
            print "SQL succeed!"
            s = "SQL succeed!\n"
            rows = cur.fetchall()
            print '\nQuestion:\n%s' % self.question
            s += 'Question:\t%s\n' % self.question
            print "Answer:"
            s += "Answer:\n"
            if self.question_type == 'location':
                print "Name\t\t\tLocation"
                s += "Name\t\t\tLocation\n"
                for row in rows:
                    print "%s\t%s" % (row[0], row[1])
                    s += "%s\t\t%s\n" % (row[0], row[1])
            if self.question_type == 'proximity_entity':
                print "Name\t\tLocation\t\tDistance(m)"
                s += "Name\t\t\tLocation\t\t\t\tDistance(m)\n"
                for row in rows:
                    print "%s\t%s\t%.2f" % (row[0], row[1], row[2])
                    s += "%s\t\t%s\t%.2f\n" % (row[0], row[1], row[2])
            if self.question_type == 'proximity_distance':
                print "From_Name\tFrom_Location\t\t\tTo_Name\t\tTo_Location\t\tDistance(m)"
                s += "From_Name\tFrom_Location\t\t\tTo_Name\t\tTo_Location\t\t\t\tDistance(m)\n"
                for row in rows:
                    print "%s\t%s\t%s\t%s\t\t%.2f" % (row[0], row[1], row[2], row[3], row[4])
                    s += "%s\t\t%s\t\t%s\t\t%s\t\t%.2f\n" % (row[0], row[1], row[2], row[3], row[4])
            if self.question_type == 'proximity_buffer':
                print "Name\t\tDistance(m)"
                s += "Name\t\tDistance(m)\n"
                for row in rows:
                    print "%s\t\t%.2f" % (row[0], row[1])
                    s += "%s\t\t%.2f\n" % (row[0], row[1])
        except Exception, e:
            print str(e)
            print "SQL not succeed!"
            s = "SQL not succeed!"
            self.conn.rollback()
        return s
