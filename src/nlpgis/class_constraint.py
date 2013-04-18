#!C:/ArcGISPython27/ArcGIS10.1/python.exe

class QuantityConstraint():
    def __init__(self, value):
        Constraint.__init__(self)
        self.value = None
        self.unit = None

class QualityConstraint():
    def __init__(self, value_lst):
        Constraint.__init__(self)
        self.values = value_lst
