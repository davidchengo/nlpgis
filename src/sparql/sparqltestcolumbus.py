'''
Created on Apr 13, 2013

@author: Administrator
'''
from SPARQLWrapper import SPARQLWrapper, SPARQLExceptions, JSON
import sys

if __name__ == '__main__':
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    sparql.setQuery("""
        PREFIX yago: <http://dbpedia.org/class/yago/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?type 
        WHERE {
         <http://dbpedia.org/resource/Columbus,_Ohio> rdf:type ?type.
        }
    """)

    results = sparql.query().convert()
    print "Number of results:",len(results), results
    geotypes=[]
    for result in results["results"]["bindings"]:
        uri=result["type"]["value"]
        value=uri.rpartition('/')[-1]
        geotypes.append(value)
        print "URI:%s\t\t\t\tValue:%s" % (uri,value)
        
    if "City" in geotypes:
        print "\nConclusion:Columbus is a city type.";