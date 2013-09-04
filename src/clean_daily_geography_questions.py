from Tkinter import *
from tkFont import *
from nltk import *
from nltk.tag.stanford import POSTagger
PATH_TO_TAGGER = os.path.join(os.getcwd(), "lib\\english-left3words-distsim.tagger")
PATH_TO_JAR = os.path.join(os.getcwd(), "lib\\stanford-postagger.jar")
st = POSTagger(PATH_TO_TAGGER,PATH_TO_JAR)
with open("grade 5 questions only.txt",'r') as fr:
    with open("grade 5 questions only clean.txt",'w') as fw:
        for line in fr.readlines():
            line=line.strip()
            if line=="":
                continue
            if line[0].isdigit():   # the first letter is a number
                line=line[2:].strip()
                question_mark_position=line.rfind("?") # breakpoints in backward order
                if question_mark_position<>-1:
                    line=line[:question_mark_position+1].strip()
                    while(line.find("  ")<>-1):
                        line=line.replace("  "," ")
                    print line
                    fw.write(line+"\n")
            if line.split()[0].lower()=="name":
                print
                fw.write("\n")
# s="Where is the nearest restaurant to the campus?"
# tagged_question=st.tag(word_tokenize(s))
# print "POS tagging:",' '.join([ w+'/'+t for w,t in tagged_question])
