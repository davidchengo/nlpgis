'''
Created on Nov 2, 2012

@author: davidchen
'''
import glob
import os, time
import csv
import codecs

from psycopg2 import connect

if __name__ == '__main__':
    os.chdir("/home/davidchen/Linktoproject/NLTK/geonames/2/")
    conn=connect("dbname=geoname user=postgres password=ohiostate") 
    cur=conn.cursor()
    count=0
    for file in glob.glob("*.txt"):     # get file name, same as database name
        if file<>'ANTARCTICA_20121001.txt':
            continue
        
        table_name = file.split('.')[0].lower()
        print table_name
        start = time.clock()
        # creating a POINT Geometry column
        try:
            sql = "SELECT AddGeometryColumn('%s', '%s', 4326, 'POINT', 2)"%(table_name,"geom")
            print sql
            cur.execute(sql)    
            conn.commit()
            print "0. geom column created... done"
        except Exception,e:
            print str(e)
            conn.rollback()
        try:
            geom = "GeomFromText('POINT('||PRIMARY_LONGITUDE_DEC||' '||PRIMARY_LATITUDE_DEC||')',4326)"
            sql="UPDATE %s SET GEOM=%s WHERE GEOM IS NULL;"%(table_name,geom)
            print sql
            cur.execute(sql)
            conn.commit()
            print "1. geom updated... done"
        except Exception,e:
            print str(e)
            conn.rollback()
        try:
            # create spatial index
            sql="CREATE INDEX %s_gix ON %s USING GIST (%s);"%(table_name,table_name,'geom')
            print sql
            cur.execute(sql)
            conn.commit()
            print "2. spatial index created...done"
        except Exception,e:
            print str(e)
            conn.rollback()
            
        try:    
            # create index 
            sql = "CREATE INDEX IDX_NAME_CLASS_%s ON %s (%s)"\
                % (table_name,table_name, "feature_name,feature_class")
            print sql
            cur.execute(sql)
            conn.commit()   
            print '3. index IDX_NAME_CLASS_'+table_name+" created."
        except Exception,e:
            print str(e)
            conn.rollback()
            
        print 'Done',table_name
        count+=1
        print "Table %d updated. Takes %.2f seconds."%(count,time.clock() - start)
        print
    cur.close()
    conn.close()
    quit()