import os
from nltk import *
from nltk.tag.stanford import POSTagger
from nltk.stem.wordnet import WordNetLemmatizer
#"lib\\english-left3words-distsim.tagger"
PATH_TO_TAGGER = os.path.join(os.getcwd(), "lib\\english-caseless-left3words-distsim.tagger")
PATH_TO_JAR = os.path.join(os.getcwd(), "lib\\stanford-postagger.jar")
stanford_tagger = POSTagger(PATH_TO_TAGGER,PATH_TO_JAR)
question_types=[]   # "what","which","where","how many","yes or no","other"
target_nouns=[]
all_other_nouns=[]
all_verbs=[]
all_prepositions=[]
all_others=[]  # word/pos
fw_d=[]
names=["question type","target nouns","other nouns","verb","prepositions","other words"]
for i in xrange(len(names)):
    fw_d.append(open("grade 5 questions stats "+names[i]+" duplicated.txt","w"))
fw_u=[]
for i in xrange(len(names)):
    fw_u.append(open("grade 5 questions stats "+names[i]+" unique.txt","w"))
count=0
with open("grade 5 questions only clean.txt",'r') as fr:
    for line in fr.readlines():
#         if line.find("border")==-1:
#             continue
        question_type=""
        target_noun=""
        other_nouns=set([])
        proper_nouns=set([])
        verbs=set([])
        prepositions=set([])
        others=set([])
        line=line.strip()   # convert all words to lower case
        if line=="":
            continue
        # find question type
        words=word_tokenize(line)
        if words[0].lower() in ["is","are"]:
            question_type="yes or no"
        else:
            frontest_wh=""
            frontest_position=9999
            for wh_word in ["what","which","where","how many"]:
                current_position=line.lower().find(wh_word)
                if(current_position<>-1) and current_position<frontest_position:
                    frontest_position=current_position
                    frontest_wh=wh_word
            if frontest_wh<>"":
                question_type=frontest_wh
            else:
                question_type="other"

        tagged=stanford_tagger.tag(words)
        #tagged=pos_tag(words)
        #print tagged
#         continue
        for w,t in tagged:
            if t in ["NN","NNS"]:
                if target_noun<>"" and w<>target_noun:
                    other_nouns.add(WordNetLemmatizer().lemmatize(w.lower(),'n'))
                else:
                    target_noun=WordNetLemmatizer().lemmatize(w.lower(),'n')
            elif t in ["VB","VBP","VBZ"]:   # base or present form
                verbs.add(WordNetLemmatizer().lemmatize(w.lower(),'v'))
            elif t in ["IN"]:
                prepositions.add(w.lower())
            else:
                if w.lower() not in other_nouns.union(verbs).union(prepositions) \
                    and w.lower()<>target_noun and w.lower()<>question_type \
                    and w.lower()<>"?":        # all those words that haven't shown up before 
                    others.add(w.lower())
#         print line
#         print tagged
#         print question_type,target_noun,other_nouns, verbs,prepositions,others
#         print
        question_types.append(question_type)
        target_nouns.append(target_noun)
        all_other_nouns+=list(other_nouns)
        all_verbs+=list(verbs)
        all_prepositions+=list(prepositions)
        all_others+=list(others)
        count+=1
        print count
#         if count>2:break
    fw_d[0].write(",".join(question_types))
    fw_d[1].write(",".join(target_nouns))
    fw_d[2].write(",".join(all_other_nouns))
    fw_d[3].write(",".join(all_verbs))
    fw_d[4].write(",".join(all_prepositions))
    fw_d[5].write(",".join(all_others))
    for w in set(question_types):
        fw_u[0].write(w+"\t"+str(question_types.count(w))+"\n")
    for w in set(target_nouns):
        fw_u[1].write(w+"\t"+str(target_nouns.count(w))+"\n")
    for w in set(all_other_nouns):
        fw_u[2].write(w+"\t"+str(all_other_nouns.count(w))+"\n")
    for w in set(all_verbs):
        fw_u[3].write(w+"\t"+str(all_verbs.count(w))+"\n")
    for w in set(all_prepositions):
        fw_u[4].write(w+"\t"+str(all_prepositions.count(w))+"\n")
    for w in set(all_others):
        fw_u[5].write(w+"\t"+str(all_others.count(w))+"\n")
    
    
        