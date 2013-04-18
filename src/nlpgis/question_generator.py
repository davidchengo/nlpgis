with open("questions.txt", 'w') as fw:
    heading = """
#1\tLocation Question
Where BE X? 
"""
    fw.write(heading)  
    # 1. Where [is] X?
    wh_lst = ['where']
    be_lst = ['is', 'are']
    for wh in wh_lst:
        for be in be_lst:
            line = wh + ' ' + be + ' ' + 'X\n'
            fw.write(line)
    
    wh_lst = ['where']
    be_lst = ['is', 'are']
    vbn_lst = ['located']
    for wh in wh_lst:
        for be in be_lst:
            for vbn in vbn_lst:
                line = wh + ' ' + be + ' ' + 'X' + ' ' + vbn + '\n'
                fw.write(line)
    
    # 2. What are the CD JJS NNS IN X?    parameters CD, JJS, NNS X
    heading = """
#2\tProximity Entity Question
What|Where|Which are the CD JJS NNS IN X? 
"""
    fw.write(heading)    
    wh_lst = ['where', 'what', 'which']
    be_lst = ['is', 'are']
    cd_lst = ['CD', '']
    jjs_lst = ['nearest', 'closest', 'close-by', 'nearby', 'neighboring',
             'distant', 'farthest', 'furthest', 'remote']
    nns_lst = ['NNS']
    in_lst = ['from', 'to', 'around', 'near', 'by', 'neighboring']
    for wh in wh_lst:
        for be in be_lst:
            for cd in cd_lst:
                for jjs in jjs_lst:
                    for nns in nns_lst:
                        for _in in in_lst:
                            line = "%s %s the %s %s %s %s X\n" % \
                            (wh, be, cd, jjs, nns, _in,)
                            fw.write(line)
    
    # 3. What CD NNS are the JJS IN X        parameters CD, JJS, NNS X
    heading = """
#3\tProximity Entity Question
What|Which CD NNS are the JJS IN X? 
"""
    fw.write(heading)
    for wh in wh_lst:
        for be in be_lst:
            for cd in cd_lst:
                for jjs in jjs_lst:
                    for nns in nns_lst:
                        for _in in in_lst:
                            line = "%s %s %s %s the %s %s X\n" % \
                            (wh, cd, nns, be, jjs, _in,)
                            fw.write(line)
    
    # 4. What be the distance IN X CC Y        parameters X and Y
    heading = """
#4\tProximity Distance Question
What be the distance between|from X and|to Y  
"""
    fw.write(heading)    
    wh_lst = ['what']
    be_lst = ['is']
    for wh in wh_lst:
        for be in be_lst:
            line = "%s %s the distance between X and Y\n" % \
            (wh, be)
            fw.write(line)
            line = "%s %s the distance from X to Y\n" % \
            (wh, be)
            fw.write(line)
    
    # 5. How far is it from X to Y?                parameters X and Y
    heading = """
#5\tProximity Distance Question
How JJ is it from X to Y  
"""
    fw.write(heading)    
    wh_lst = ['how']
    jj_lst = ['far', 'distant']
    is_it_lst = ['is it', '']
    for wh in wh_lst:
        for jj in jj_lst:
            for is_it in is_it_lst:
                for _in in in_lst:
                    line = "%s %s %s between X and Y\n" % \
                    (wh, jj, is_it)
                    fw.write(line)
                    line = "%s %s %s from X to Y\n" % \
                    (wh, jj, is_it)
                    fw.write(line)
                    
                    
    # 5. How far is X from Y?                parameters X and Y
    heading = """
#5\tProximity Distance Question
How JJ is X from|to Y  
"""
    fw.write(heading)    
    wh_lst = ['how']
    jj_lst = ['far', 'distant']
    be_lst = ['is']
    in_lst = ['from', 'to']
    for wh in wh_lst:
        for jj in jj_lst:
            for be in be_lst:
                for _in in in_lst:
                    line = "%s %s %s X %s Y\n" % \
                    (wh, jj, be, _in)
                    fw.write(line)
       
    # What cities are within N units from X?
    heading = """
#\tProximity Buffer Question
What NNS be within|inside CD NNS RB IN X
e.g. What cities are within 100 miles from Columbus?  
"""
    fw.write(heading)    
    wh_lst = ['what', 'how many']
    nns_lst = ['NNS']
    be_lst = ['is']
    in1_lst = ['within', 'inside', 'outside']
    cd_lst = ['CD']
    unit_lst = ['miles', 'kilometers', 'kilometres', 'meters']
    in2_lst = ['from', 'of', 'to']
    
    for wh in wh_lst:
        for nns in nns_lst:
            for be in be_lst:
                for in1 in in1_lst:
                    for cd in cd_lst:
                        for unit in unit_lst:
                            for in2 in in1_lst:
                                line = "%s %s %s %s %s %s %s Y\n" % \
                                (wh, nns, be, in1, cd, unit, in2)
                                fw.write(line)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
