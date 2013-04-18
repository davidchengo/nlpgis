#!C:/ArcGISPython27/ArcGIS10.1/python.exe

class Data(object):  # super class. Use a new-style class inherited from object
    type_value_dict = {'city':['Columbus', 'Dayton']}
    def __init__(self):
        self.type = 'Unknown'
        self.value_lst = []  # value is the name of the type of data. e.g. Columbus is a name value of the city type
        self.constraint = None
    def set_type(self, type):  # type is deterministic
        self.type = type 
    def resolve_type(self, w):  # type is vague
        for key, values in InputData.type_value_dict.iteritems():
            if w in Data.type_value_dict[key]:
                self.type = key
    def add_value(self, value):
        self.value_lst.append(value)

    
class InputData(Data):    
    def __init__(self):
        super(InputData, self).__init__()
    def to_str(self):
        s = "Input Data: %s -> " % self.type
        for v in self.value_lst:
            s += "%s " % v
        return s
    
class OutputData(Data):
    def __init__(self):
        super(OutputData, self).__init__()
        self.count = 1
    def to_str(self):
        s = "Output Data: %s." % (self.type)
        return s
    def set_count(self, count):
        self.count = count
      
class Relation:
    def __init__(self):
        self.tagged = None
        self.term = None
        self.super_type = None  # proximity
        self.type = None  # buffer
        self.constraint = None  # an constraint object
        self.order = None
        
    def set_type(self, type):
        self.type = type
        if type in ['distance', 'buffer']:
            self.super_type = 'proximity'
       
    def resolve_type(self, w):
        if w in ['nearest', 'closest']:
            self.order = 'ASC'
            self.type = 'distance.nearest'
            self.super_type = 'proximity'
        elif w in ['farthest', 'furthest']:
            self.order = 'DESC'
            self.type = 'distance.fartheset'
            self.super_type = 'proximity'
            
    def to_str(self):
        return "%s.%s" % (self.super_type, self.type)
    
class Constraint(object):  # all other field values except name, such as population. Constraints on relation has types of distance, etc
    def __init__(self):
        self.super_type = None
        self.type = type
        self.value_lst = []
    def add_value(self, value):
        self.value_lst.append(value)
    def set_super_type(self, super_type):
        self.super_type = super_type
    def set_type(self, type):
        self.type = type
        
class QuantityConstraint(Constraint):
    def __init__(self):
        super(QuantityConstraint, self).__init__()
        self.unit_lst = []
        self.operator_lst = []
    def to_str(self):
        s = ''
        for i in xrange(len(self.value_lst)):
            s += "%s %s %.0f %s. " % (self.type, self.operator_lst[i], self.value_lst[i], self.unit_lst[i])
        return s
    def add_operator(self, optr):
        self.operator_lst.append(optr)
    def add_unit(self, unit):
        self.unit_lst.append(unit)
        
class QualityConstraint(Constraint):
    def __init__(self):
        super(QuantityConstraint, self).__init__(type)
    def to_str(self):
        s = ''
        for i in xrange(len(self.value_lst)):
            value = self.value_lst[i]
            s += "%s is %s. " % (self.type, value)
        return s
