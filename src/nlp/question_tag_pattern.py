from nltk import word_tokenize
from nltk.tag.stanford import POSTagger
PATH_TO_TAGGER = r'C:\\AptanaWorkspace\\Thesis\\src\\lib\\english-left3words-distsim.tagger'
PATH_TO_JAR = r'C:\\AptanaWorkspace\\Thesis\\src\\lib\\stanford-postagger.jar'
stanford_tagger = POSTagger(PATH_TO_TAGGER, PATH_TO_JAR)
count = 1
with open('question_w_t.txt', 'w') as fw:
    sent_lst = []
    with open('question_word.txt', 'r') as fr:
        while(1):
            line = fr.readline()
            line = line.strip()
            if line == '':
                out_lst = list(set(sent_lst))
                fw.write('\n'.join(out_lst))
                print '\n'.join(out_lst)
                break
            if line[0] <> '#':
                # tag_lst=[a[1] for a in stanford_tagger.tag(word_tokenize(line))]
                tag_lst = ['/'.join(a) for a in stanford_tagger.tag(word_tokenize(line))]
                # print tag_lst
                sent_lst.append(' '.join(tag_lst))
            else:
                out_lst = list(set(sent_lst))
                fw.write('\n' + '\n'.join(out_lst) + '\n')
                fw.write(line)
                print '\n'.join(out_lst)
                print line
                sent_lst = []
            count += 1
            if count % 100 == 0:
                print count
