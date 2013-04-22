from Tkinter import *
from tkFont import *
from nltk import *
from nltk.tag.stanford import POSTagger
PATH_TO_TAGGER = r'../lib/english-left3words-distsim.tagger'
PATH_TO_JAR = r'../lib/stanford-postagger.jar'
tagger = POSTagger(PATH_TO_TAGGER,PATH_TO_JAR)
count=0

with open("question.txt",'r') as fr:
    with open("question_tagged",'w') as fw1:
        with open("question_word_tagged",'w') as fw2:
            while(1):
                line=fr.readline()
                line=line.strip()
                if line=='':    # EOF
                    break
                if line[0]=='#':
                    line+='\n'
                    fw1.write(line)
                    fw2.write(line)
                    print line
                    count=0
                else:
                    tagged_question=tagger.tag(word_tokenize(line))
                    tag_seq=' '.join([t for w,t in tagged_question])+'\n'
                    fw1.write(tag_seq)
                    word_tag_seq=' '.join([w+'/'+t for w,t in tagged_question])+'\n'
                    fw2.write(word_tag_seq)
                    count+=1
                    print count
                