with open("question_word.txt", 'w') as fw:
    heading = """#1\tLocation Question\n"""
    fw.write(heading)  
    # 1. Where [is] Columbus?
    line = 'Where is Columbus?\n'
    fw.write(line)
    line = 'Where are Columbus and Dayton?\n'
    fw.write(line)
    
    line = 'Where is Columbus located?\n'
    fw.write(line)
    line = 'Where are Columbus and Dayton located?\n'
    fw.write(line)
    
    # 2. What are the CD JJS NNS IN Columbus?    parameters CD, JJS, NNS Columbus
    heading = """#2\tProximity Entity Question"""
    fw.write(heading)    
    wh_lst = ['where', 'what', 'which']
    be_lst = ['are']
    cd_lst = ['3', 'three']
    jjs_lst = ['nearest', 'closest', 'close-by', 'nearby', 'neighboring',
             'distant', 'farthest', 'furthest', 'most remote']
    nns_lst = ['cities']
    in_lst = ['from', 'to', 'around', 'near', 'by']
    for wh in wh_lst:
        for be in be_lst:
            for cd in cd_lst:
                for jjs in jjs_lst:
                    for nns in nns_lst:
                        for _in in in_lst:
                            line = "%s %s the %s %s %s %s Columbus\n" % \
                            (wh, be, cd, jjs, nns, _in)
                            fw.write(line)
                            
    # 3. What CD NNS are the JJS IN Columbus        parameters CD, JJS, NNS Columbus
    for wh in wh_lst:
        for cd in cd_lst:
            for nns in nns_lst:
                for be in be_lst:
                    for jjs in jjs_lst:
                        for nns in nns_lst:
                            for _in in in_lst:
                                line = "%s %s %s %s the %s %s Columbus\n" % \
                                (wh, cd, nns, be, jjs, _in)
                                fw.write(line)
    # singular form                    
    wh_lst = ['where', 'what', 'which']
    be_lst = ['is']
    jjs_lst = ['nearest', 'closest', 'close-by', 'nearby', 'neighboring',
             'distant', 'farthest', 'furthest', 'most remote']
    nn_lst = ['city']
    in_lst = ['from', 'to', 'around', 'near', 'by']
    for wh in wh_lst:
        for be in be_lst:
            for cd in cd_lst:
                for jjs in jjs_lst:
                    for nn in nn_lst:
                        for _in in in_lst:
                            line = "%s %s the %s %s %s Columbus\n" % \
                            (wh, be, jjs, nn, _in,)
                            fw.write(line)
    
    for wh in wh_lst:
        for nn in nn_lst:
            for be in be_lst:
                for jjs in jjs_lst:
                    for _in in in_lst:
                        line = "%s %s %s the %s %s Columbus\n" % \
                        (wh, nn, be, jjs, _in)
                        fw.write(line)

    
    # 4. What be the distance between|from Columbus and|to Dayton          parameters Columbus and Dayton
    heading = """#3\tProximity Distance Question"""
    fw.write(heading)    
    wh_lst = ['what']
    be_lst = ['is']
    for wh in wh_lst:
        for be in be_lst:
            line = "%s %s the distance between Columbus and Dayton\n" % \
            (wh, be)
            fw.write(line)
            line = "%s %s the distance from Columbus to Dayton\n" % \
            (wh, be)
            fw.write(line)
    
    # 5. How far is it from Columbus to Dayton?                parameters Columbus and Dayton  
    wh_lst = ['how']
    jj_lst = ['far']
    is_it_lst = ['is it']
    for wh in wh_lst:
        for jj in jj_lst:
            for is_it in is_it_lst:
                for _in in in_lst:
                    line = "%s %s %s between Columbus and Dayton\n" % \
                    (wh, jj, is_it)
                    fw.write(line)
                    line = "%s %s %s from Columbus to Dayton\n" % \
                    (wh, jj, is_it)
                    fw.write(line)
                    
                    
    # 5. How far is Columbus from Dayton?                parameters Columbus and Dayton  
    wh_lst = ['how']
    jj_lst = ['far']
    be_lst = ['is']
    in_lst = ['from', 'to']
    for wh in wh_lst:
        for jj in jj_lst:
            for be in be_lst:
                for _in in in_lst:
                    line = "%s %s %s Columbus %s Dayton\n" % \
                    (wh, jj, be, _in)
                    fw.write(line)
       
    # What NNS be within|inside CD NNS RB IN Columbus
    # e.g. What cities are within 100 miles from Columbus?  
    heading = """#4\tProximity Buffer Question"""
    fw.write(heading)    
    wh_lst = ['what', 'how many']
    nns_lst = ['cities']
    be_lst = ['are']
    in1_lst = ['within', 'inside', 'outside']
    cd_lst = ['20', 'twenty']
    unit_lst = ['miles', 'kilometers', 'kilometres', 'meters']
    in2_lst = ['from', 'of', 'to']
    
    for wh in wh_lst:
        for nns in nns_lst:
            for be in be_lst:
                for in1 in in1_lst:
                    for cd in cd_lst:
                        for unit in unit_lst:
                            for in2 in in1_lst:
                                line = "%s %s %s %s %s %s %s Columbus\n" % \
                                (wh, nns, be, in1, cd, unit, in2)
                                fw.write(line)
    # singular  
    wh_lst = ['what']
    nn_lst = ['city']
    be_lst = ['is']
    in1_lst = ['within', 'inside', 'outside']
    cd_lst = ['20', 'twenty']
    unit_lst = ['miles', 'kilometers', 'kilometres', 'meters']
    in2_lst = ['from', 'of', 'to']
    
    for wh in wh_lst:
        for nn in nn_lst:
            for be in be_lst:
                for in1 in in1_lst:
                    for cd in cd_lst:
                        for unit in unit_lst:
                            for in2 in in1_lst:
                                line = "%s %s %s %s %s %s %s Columbus\n" % \
                                (wh, nn, be, in1, cd, unit, in2)
                                fw.write(line)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
