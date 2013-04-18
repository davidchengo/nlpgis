#!C:/ArcGISPython27/ArcGIS10.1/python.exe

class SQLConfig:
	base_form = {
"proximity_entity":"""
SELECT t_out.name As name, ASTEXT(t_out.geom) As location, 
ST_Distance(ST_Transform(t_in.geom,2163),ST_Transform(t_out.geom,2163)) as dist
FROM ohio_place As t_in, ohio_place As t_out   
""",
"proximity_distance":"""
SELECT t_in1.name As from_name, ASTEXT(t_in1.geom) As from_loc,t_in2.name As to_name, ASTEXT(t_in2.geom) As to_loc, 
ST_Distance(ST_Transform(t_in1.geom,2163),ST_Transform(t_in2.geom,2163)) as dist
FROM ohio_place As t_in1, ohio_place As t_in2   
WHERE t_in1.name ='%s' and t_in2.name ='%s' 
"""
			}
	
	where_clause = {
"proximity_entity":"""
WHERE t_in.name IN (%s) and t_in.id <> t_out.id  
"""
}
	
	order_by_clause = {
"proximity_entity":"""
ORDER BY dist %s
"""
}
	
	limit_clause = {
"proximity_entity":"""
LIMIT %d
"""}
	
	def __init__(self):
		self.output = None  # an Data object\
		self.input = None
		self.relation = None
