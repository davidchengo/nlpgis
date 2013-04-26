#!C:/ArcGISPython27/ArcGIS10.1/python.exe

class Data(object):  # super class. Use a new-style class inherited from object
    type_lst = ['city','town','village']
    def __init__(self):
        self.category = 'location'      # default type
        self.value_lst = []  # value is the name of the type of data. e.g. Columbus is a name value of the city type
        self.constraint_lst = []
    def value2quoted(self):
        return "'" + "','".join(self.value_lst) + "'"
    
class InputData(Data):    
    def __init__(self):
        super(InputData, self).__init__()
    def to_str(self):
        s = "Input: "
        s += ','.join(self.value_lst)
        return s
    def bufferconstraint2sql(self):
        dist_lst=[]
        for constraint in self.constraint_lst:
            if constraint.__class__.__name__=='QuantityConstraint':
                if constraint.category=='buffer':
                    if constraint.unit in ['meters','ms','metres','meter','m']:
                        dist_lst.append(float(constraint.value))
                    elif constraint.unit in ['kms', 'km', 'kilometers', 'kilometer']:
                        dist_lst.append(float(constraint.value)*1000)
                    elif constraint.unit in ['mile', 'miles','mi','mis']:
                        dist_lst.append(float(constraint.value)*1609.34)
        s=''
        if len(dist_lst)==1:       # within 10 miles of Columbus and Dayton
            s+="""
t_out.name in 
(select t_out.name 
from ohio_place As t_out, ohio_place As t_in  
where t_in.name IN ('%s') and t_out.name not IN (%s) 
AND ST_Within(ST_Transform(t_out.geom,2163),ST_Buffer(ST_Transform(t_in.geom,2163),%.2f))
)""" % (self.value_lst[0],self.value2quoted(),dist_lst[0])
            if len(self.value_lst)==2:
                s+="""
AND
t_out.name in
(select t_out.name 
from ohio_place As t_out, ohio_place As t_in  
where t_in.name IN ('%s') and t_out.name not IN (%s) 
AND ST_Within(ST_Transform(t_out.geom,2163),ST_Buffer(ST_Transform(t_in.geom,2163),%.2f))
)
""" % (self.value_lst[1],self.value2quoted(),dist_lst[0])
        elif len(dist_lst)>1:
            s+="""
t_out.name in 
(select t_out.name 
from ohio_place As t_out, ohio_place As t_in  
where t_in.name IN ('%s') and t_out.name not IN (%s) 
AND ST_Within(ST_Transform(t_out.geom,2163),ST_Buffer(ST_Transform(t_in.geom,2163),%.2f))
)
AND
t_out.name in
(select t_out.name 
from ohio_place As t_out, ohio_place As t_in  
where t_in.name IN ('%s') and t_out.name not IN (%s) 
AND ST_Within(ST_Transform(t_out.geom,2163),ST_Buffer(ST_Transform(t_in.geom,2163),%.2f))
)
""" % (self.value_lst[0],self.value2quoted(),dist_lst[0],
       self.value_lst[1],self.value2quoted(),dist_lst[1])

        return s
    
class OutputData(Data):
    def __init__(self):
        super(OutputData, self).__init__()
        self.count = 1
        self.order = 'ASC'      # default output order: ASC
    def to_str(self):
        s = "Output: %s. Constraints: " % self.category
        if len(self.constraint_lst)>0:
            for constraint in self.constraint_lst:
                if constraint.__class__.__name__=='QuantityConstraint':
                    s+="%s:%s %s, %s" % (constraint.category,constraint.value,constraint.unit,constraint.operator)
                elif constraint.__class__.__name__=='QualityConstraint':
                    s+="%s is %s" %(constraint.category,constraint.value)
                else:
                    print "Shouldn't get here. Output constraint.."
        else:
            s+='None'
        return s
    def qualityconstraint2sql(self,table):
        s=''
        for constraint in self.constraint_lst:
            if constraint.__class__.__name__=='QualityConstraint':
                if constraint.value in ['big','major','large','principal']:
                    s+=" AND %s.type in ('city')" % (table)
                elif constraint.value in ['small','secondary']:
                    s+=" AND %s.type in ('village','town')" % (table)
        return s
       
class Relation:
    def __init__(self,category=None,constraint=None):
        self.category = category            # buffer
        self.constraint = constraint        # an constraint object     
    def to_str(self):
        return "Relation: %s" % (self.category)
    
class Constraint(object):  # all other field values except name, such as population. Constraints on relation has types of distance, etc
    def __init__(self,value=None,category=None):
        # number or modifier
        self.value = value
        # buffer, population
        self.category=category
        
class QuantityConstraint(Constraint):
    def __init__(self,value=None,category=None,unit=None,operator=None):     # 10, buffer, miles, intersect/disjoint
        super(QuantityConstraint, self).__init__(value,category)     # modify here
        self.unit = unit
        self.operator = operator
        
class QualityConstraint(Constraint):
    population_constraint=['big', 'major','large','principal','small','secondary']
    def __init__(self,value=None,category=None):
        super(QualityConstraint, self).__init__(value,category)
