from nltk.tag.stanford import POSTagger
from psycopg2 import connect
from nltk import word_tokenize
PATH_TO_TAGGER = r'../lib/english-left3words-distsim.tagger'
PATH_TO_JAR = r'../lib/stanford-postagger.jar'
tagger = POSTagger(PATH_TO_TAGGER,PATH_TO_JAR)
count=0
conn = connect("dbname=Ohio user=postgres password=ohiostate")
cur = conn.cursor()
# tag new sentences and update the database
question_type_id=None
with open("new_question",'r') as fr:
    while(1):
        line=fr.readline()
        line=line.strip()
        if line=='':    # EOF
            break
        if line[0]=='#':
            question_type_id=int(line.split(' ')[1])
            print question_type_id,line
            count=0
        else:
            tagged_question=tagger.tag(word_tokenize(line))
            tag=' '.join([t for w,t in tagged_question])
            tagged=' '.join([w+'/'+t for w,t in tagged_question])
            try:
                sql = """INSERT INTO template (tag, question_type_id) values ('%s',%d)""" % \
                    (tag,question_type_id)
                print sql
                cur.execute(sql)    
                conn.commit()
            except Exception,e:
                print str(e)
                conn.rollback()
            try:
                sql = """INSERT INTO question (sentence,tagged,tag,question_type_id) values ('%s','%s','%s',%d)""" % \
                    (line.replace("'", "''"),tagged.replace("'", "''"),tag,question_type_id)
                print sql
                cur.execute(sql)    
                conn.commit()
            except Exception,e:
                print str(e)
                conn.rollback()
            count+=1
            print count
                