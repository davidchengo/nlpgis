'''
Created on Nov 2, 2012

@author: davidchen
'''
import sqlite3
import string
import glob
import os, sys,time
import csv
import codecs
from pyspatialite import dbapi2 as db

if __name__ == '__main__':
    os.chdir("/home/davidchen/Linktoproject/NLTK/geonames/1/")
    
    mydatabase="/home/davidchen/Linktoproject/NLTK/geonames.sqlite"
    # creating/connecting the test_db
    conn = db.connect(mydatabase)
    # creating a Cursor
    cur = conn.cursor()
    count=0
    for file in glob.glob("*.txt"):
        table_name = file.split('.')[0]
        start = time.clock()
        # creating a POINT Geometry column
        try:
            sql = "SELECT AddGeometryColumn('"+table_name+"', "
            sql += "'geom', 4326, 'POINT', 'XY')"
            cur.execute(sql)
            print sql
            conn.commit()
            geom = "GeomFromText('POINT('||PRIM_LONG_DEC||' '||PRIM_LAT_DEC ||')',4326)"
            sql="UPDATE "+table_name+" SET GEOM="+geom+" WHERE GEOM IS NULL"
            print sql
            cur.execute(sql)
            conn.commit()
            print "geom updated... done"
            # create spatial index
            sql="SELECT CreateSpatialIndex('"+table_name+"', 'geom');"
            print sql
            cur.execute(sql)
            conn.commit()
            print "spatial index created...done"
            
            # create index 
            sql = "CREATE INDEX IF NOT EXISTS IDX_NAME_CLASS_"+table_name.split('_')[0]+" ON "\
                + table_name + " (feature_name,feature_class)"
            print sql
            cur.execute(sql)
            conn.commit()   
            print 'index IDX_NAME_CLASS_'+table_name.split('_')[0]+" created."
        except:
            print "Unexpected error:", sys.exc_info()[0]
        print '\ndone',table_name
        count+=1
        print count,':',time.clock() - start
        print
        #exit(0)