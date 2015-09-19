#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import cgi
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
Myfile.close

try:
	comm = psycopg2.connect(database = dbname, host = host, user = user, password = pas)
except:
	sys.exit("Error! Can not connecto to database!")

cur = comm.cursor()
cur.execute("SELECT nome_stazione, min(comune) as comune, min(provincia) as provincia, min(regione) as regione, min(longitudine) as longitudine, min(latitudine) as latitudine FROM temporaneatab GROUP BY nome_stazione ORDER BY nome_stazione asc")
righe = cur.fetchall()

ctrl=0
datiGEOJSON = ""    
datiGEOJSON = str(datiGEOJSON)+"{\"type\":\"FeatureCollection\",\"features\":[\n"
for riga in righe:
	if ctrl:
        	datiGEOJSON = str(datiGEOJSON)+","
        else:
            	ctrl=1
        datiGEOJSON = str(datiGEOJSON)+"{\"type\": \"Feature\",\"geometry\":{\"type\": \"Point\",\"coordinates\":["+str(riga[4])+","+str(riga[5])+"]},"
        datiGEOJSON = str(datiGEOJSON)+"\"properties\":{\"comune\":\""+riga[1]+"\",\"provincia\":\""+riga[2]+"\",\"regione\":\""+riga[3]+"\"}}\n"
    datiGEOJSON = str(datiGEOJSON)+"]}"
    
comm.close()
print "Content-type:text/geojson\n"
print datiGEOJSON
