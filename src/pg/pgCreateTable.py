'''
Created on Nov 6, 2012

@author: davidchen
'''

import psycopg2
import glob,os,csv,sys
import StringIO
from time import time

def unicode_csv_reader(unicode_csv_data, delimiter=',',dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            delimiter=delimiter,
                            dialect=dialect, **kwargs)
    return csv_reader
#    for row in csv_reader:
#        # decode UTF-8 back to Unicode, cell by cell:
#        yield [unicode(cell, 'utf-8') for cell in row]
        

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

def timer():
    global start
    print "%0.2f" % (time()-start)
    start=time()

def create_populate_table(table_name,fields,types,cur):
    #print table_name+" not exists"
    sql = 'CREATE TABLE IF NOT EXISTS %s (\n'%(table_name) 
    for i in xrange(len(fields)):
        if i==0:
            sql += "%s %s,\n"%(fields[i],types[i])
        elif i==len(fields)-1:
            sql += "%s %s,\n PRIMARY KEY (%s,%s,%s))"%(fields[i],types[i],'FEATURE_ID','COUNTY_NUMERIC','STATE_NUMERIC')
        else:
            sql += "%s %s,\n"%(fields[i],types[i])
    print sql
    try:
        cur.execute(sql)
        conn.commit()
    except Exception,e:
        print str(e)
        conn.rollback()
    print "Table ",table_name," created ",timer()
    
    cur.execute("SELECT count(*) from "+table_name)
    if cur.fetchone()[0]>0:
        return
    # populate data into created table
    fr= open(file, 'r')
    fr.readline()
    # parse and convert data into unicode
    #data = unicode_csv_reader(fr, delimiter='|')
    # anything can be used as a file if it has .read() and .readline() methods
    data = StringIO.StringIO()
    s=''.join(fr.readlines())
    while(s.find('\0')<>-1):
        j=s.find('\0')
        #print "%d'%s'"%(j,s[j-1:j+10])
        #print j
        #print "%s,'%s\'"%(s[j-100:j+100],s[j-1:j+1])
        s=s.replace('\0','')
    while(s.find('\\|')<>-1):
        s=s.replace('\\|','|')
    while(s.find('\r\n')<>-1):
        s=s.replace('\r\n','\n')
    while(s.find('\r\n')<>-1):
        s=s.replace('\r\n','\n')
    #timer()
    while(s.find('||')<>-1 or s.find('|\n')<>-1 ):
        s=s.replace('||','|0|')
        s=s.replace('|\n','|0\n')
    #timer()
    #print s.split('\t')[:2]
    #exit(0)
    data.write(s)
    data.seek(0)
    try:
        cur.copy_from(data, table_name,sep='|')
        conn.commit()
        print "Table ",table_name," populated ",timer()
    except psycopg2.DatabaseError, e:
        if conn:
            conn.rollback()
        print 'Error %s' % e    
    fr.close()    
    
global start

if __name__ == '__main__':        
#    20 fields for state featuers and national features, Populated Places, Historical Features, Concise Features
#    fields = ['FEATURE_ID', 'FEATURE_NAME', 'FEATURE_CLASS', 'STATE_ALPHA', 'STATE_NUMERIC'
#            , 'COUNTY_NAME', 'COUNTY_NUMERIC', 'PRIMARY_LAT_DMS', 'PRIM_LONG_DMS', 'PRIM_LAT_DEC'
#            , 'PRIM_LONG_DEC', 'SOURCE_LAT_DMS', 'SOURCE_LONG_DMS', 'SOURCE_LAT_DEC', 'SOURCE_LONG_DEC'
#            , 'ELEV_IN_M', 'ELEV_IN_FT', 'MAP_NAME', 'DATE_CREATED', 'DATE_EDITED']
#    types = ['NUMERIC', 'TEXT', 'TEXT', 'TEXT', 'TEXT'
#           , 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'NUMERIC'
#           , 'NUMERIC', 'TEXT', 'TEXT', 'NUMERIC', 'NUMERIC'
#           , 'NUMERIC', 'NUMERIC', 'TEXT', 'TEXT', 'TEXT']

#     ALL names
#    fields=['FEATURE_ID', 'FEATURE_NAME','FEATURE_NAME_OFFICIAL', 'CITATION','DATE_CREATED']
#    types=['NUMERIC','TEXT','TEXT','TEXT','TEXT']

#    Feature Description/History
#    fields=['FEATURE_ID', 'DESCRIPTION','HISTORY']
#    types=['NUMERIC','TEXT','TEXT']

#    fields=["ANTARCTICA_FEATURE_ID","FEATURE_NAME","FEATURE_CLASS","PRIMARY_LATITUDE_DMS", \
#            "PRIMARY_LONGITUDE_DMS","PRIMARY_LATITUDE_DEC","PRIMARY_LONGITUDE_DEC", \
#            "ELEV_IN_M","ELEV_IN_FT","DECISION_YEAR","DESCRIPTION","DATE_CREATED","DATE_EDITED"]
#    types=['NUMERIC','TEXT','TEXT','TEXT','TEXT',
#           'NUMERIC','NUMERIC','NUMERIC','NUMERIC',
#           'TEXT','TEXT','TEXT','TEXT']


    fields=["FEATURE_ID","UNIT_TYPE","COUNTY_NUMERIC","COUNTY_NAME",
            "STATE_NUMERIC","STATE_ALPHA","STATE_NAME","COUNTRY_ALPHA",
            "COUNTRY_NAME","FEATURE_NAME"]
    types=['NUMERIC','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT']
    
    global start
    start=time()
#    fields=['FEATURE_ID','FEATURE_NAME','FEATURE_NAME_OFFICIAL','CITATION','DATE_CREATED']
#    types=['NUMERIC', 'TEXT', 'TEXT', 'TEXT','NUMERIC']
    conn=psycopg2.connect("dbname=geoname user=postgres password=ohiostate") 
    cur=conn.cursor()
    cur.execute('SELECT version()')          
    ver = cur.fetchone()
    print ver   
    
    os.chdir("/home/davidchen/Desktop/Linktoproject/NLTK/geonames/2")
    for file in glob.glob("*.txt"):
        if file<>'GOVT_UNITS_20121001.txt':
            continue
        print
        print file
        #timer()
        # create table
        table_name = file.split('.')[0]
        try:
            create_populate_table(table_name,fields,types,cur)
        except psycopg2.DatabaseError, e:
            if conn:
                conn.rollback()
            print 'Error %s' % e    
        #break
    cur.close()
    conn.close()
    quit()