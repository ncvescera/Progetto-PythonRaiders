#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
#import cgi
import psycopg2

#LEGGE DA FILE SOLO LINEA PER LINEA
Myfile = open("credenziali.txt","r")
dbname= Myfile.readline()
dbname = dbname[:-1] #serve per eliminare l'ultimo carattere: \n
host = Myfile.readline()
host = host[:-1]
user = Myfile.readline()
user = user[:-1]
pas = Myfile.readline()
pas = pas[:-1]
port = Myfile.readline()
Myfile.close

connect_str = "dbname="+dbname+" host="+host+" user="+user+" password="+pas+" port="+port
try:
	comm = psycopg2.connect(str(connect_str))
except:
    	sys.exit("Error! Can not connect to the server.")

#SELECT per selezionare un campo della tabella specificata dopo FROM    
cur = comm.cursor()
cur.execute("SELECT tempo_calcolo, avg(piovuta_96) as piovuta_96 FROM spatialtemporal GROUP BY tempo_calcolo ORDER BY tempo_calcolo asc")
rows = cur.fetchall()

datiCSV = "data,Piovuta"
for row in rows:
    datiCSV = str(datiCSV)+str(row).strip("()")+"\n"

    
comm.close()

print "Content-type:text/csv\n"
print datiCSV

