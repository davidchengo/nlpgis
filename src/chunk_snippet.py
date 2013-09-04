def conll_tag_chunks(chunk_sents):
    tag_sents = [nltk.chunk.tree2conlltags(tree) for tree in chunk_sents]
    return [[(t, c) for (w, t, c) in chunk_tags] for chunk_tags in tag_sents]
     
def ubt_conll_chunk_accuracy(train_sents, test_sents):
    # train_chunks are list of pos_tag, chunk_tag pairs [[t0,c0],[t1,c1],[t2,c2],[t3,c3],...]
    train_chunks = conll_tag_chunks(train_sents)
    test_chunks = conll_tag_chunks(test_sents)
 
    u_chunker = nltk.tag.UnigramTagger(train_chunks)
    print 'u:', u_chunker.evaluate(test_chunks)
    
    ub_chunker = nltk.tag.BigramTagger(train_chunks, backoff=u_chunker)
    print 'ub:', ub_chunker.evaluate(test_chunks)
 
    ubt_chunker = nltk.tag.TrigramTagger(train_chunks, backoff=ub_chunker)
    print 'ubt:', ubt_chunker.evaluate(test_chunks)
 
#    ut_chunker = nltk.tag.TrigramTagger(train_chunks, backoff=u_chunker)
#    print 'ut:', ut_chunker.evaluate(test_chunks)
# 
#    utb_chunker = nltk.tag.BigramTagger(train_chunks, backoff=ut_chunker)
#    print 'utb:', utb_chunker.evaluate(test_chunks)
 