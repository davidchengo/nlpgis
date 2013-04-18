'''
Created on Nov 1, 2012

@author: davidchen
'''
import sqlite3
import string
import glob,os,csv
from pyspatialite import dbapi2 as db
from time import time

def unicode_csv_reader(unicode_csv_data, delimiter=',',dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            delimiter=delimiter,
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


def timer():
    global start
    print time()-start
    start=time()
           
def create_populate_table(table_name,fields,types,cur):
    print table_name+" not exists"
    sql = 'CREATE TABLE IF NOT EXISTS ' + table_name + ' (\n'
    for i in xrange(len(fields)):
        if i==1:
            sql += fields[i]+' '+types[i]+',\n'
        elif i==len(fields)-1:
            sql += fields[i]+' '+types[i]+')'
        else:
            sql += fields[i]+' '+types[i]+',\n'
    print sql
    cur.execute(sql)
    conn.commit()
    print "Create table ",table_name," costs ",timer()
    # populate data into created table
    with open(file, 'r') as fr:
        fr.readline()
        # parse and convert data into unicode
        data = unicode_csv_reader(fr, delimiter='|')
        sql='INSERT INTO '+table_name
        sql+=' values ('
        for i in xrange(len(fields)):
            if i==len(fields)-1:
                sql+="?)"
            else:
                sql+="?, "
        #print sql
        cur.executemany(sql, data)
    conn.commit()
    print "Populate table ",table_name," costs ",timer()

global start

if __name__ == '__main__':

    #20 fields national features folder1 and folder2a
#    fields = ['FEATURE_ID', 'FEATURE_NAME', 'FEATURE_CLASS', 'STATE_ALPHA', 'STATE_NUMERIC'
#            , 'COUNTY_NAME', 'COUNTY_NUMERIC', 'PRIMARY_LAT_DMS', 'PRIM_LONG_DMS', 'PRIM_LAT_DEC'
#            , 'PRIM_LONG_DEC', 'SOURCE_LAT_DMS', 'SOURCE_LONG_DMS', 'SOURCE_LAT_DEC', 'SOURCE_LONG_DEC'
#            , 'ELEV_IN_M', 'ELEV_IN_FT', 'MAP_NAME', 'DATE_CREATED', 'DATE_EDITED']
#    types = ['NUMERIC', 'TEXT', 'TEXT', 'TEXT', 'TEXT'
#           , 'TEXT', 'TEXT', 'TEXT', 'TEXT', 'NUMERIC'
#           , 'NUMERIC', 'TEXT', 'TEXT', 'NUMERIC', 'NUMERIC'
#           , 'NUMERIC', 'NUMERIC', 'TEXT', 'NUMERIC', 'NUMERIC']
    global start
    start=time()
    fields=['FEATURE_ID','FEATURE_NAME','FEATURE_NAME_OFFICIAL','CITATION','DATE_CREATED']
    types=['NUMERIC', 'TEXT', 'TEXT', 'TEXT','NUMERIC']
    #db.Connection.text_factory=unicode
    #sqlite3.Connection.text_factory = unicode
    conn=db.connect('/home/davidchen/Linktoproject/NLTK/geonames.sqlite')
    cur=conn.cursor()
    os.chdir("/home/davidchen/Linktoproject/NLTK/geonames/2/")
    for file in glob.glob("*.txt"):
        if file<>'AllNames_20121001.txt':
            continue
        print file
        timer()
        # create table
        table_name = file.split('.')[0]
        try:
            sql="SELECT count(*) FROM "+table_name
            result=cur.execute(sql)
        except:
            create_populate_table(table_name,fields,types,cur)
        if result.fetchone()[0]==0:
            print table_name+"exists but has no records"
            # if table doesn't exist or exists but has no records then create/populate table
            create_populate_table(table_name,fields,types,cur)
        
    conn.close()
    quit()