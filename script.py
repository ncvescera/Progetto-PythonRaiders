#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
import cgitb; cgitb.enable();
import psycopg2

form = cgi.FieldStorage()

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

comm = psycopg2.connect(database = dbname, host = host, user = user, password = pas)

#SELECT per selezionare un campo della tabella specificata dopo FROM    
cur = comm.cursor()
cur.execute("SELECT comune, provincia, regione, longitudine, latitudine, nome_stazione FROM temporaneatab GROUP BY nome_stazione ORDER BY nome_stazione asc")
rows = cur.fetchall()

csv = form.getvalue('CSV')

if csv:
    datiCSV = open("dati.csv","w")
    for row in rows:
        datiCSV.write(str(row).strip("()").replace(",",";"))
        datiCSV.write("\n")
 
gjson = form.getvalue('geoJson')       
if gjson:   
    datiGEOJSON = open("dati.geojson","w")  
    cur = comm.cursor()
    cur.execute("SELECT comune, provincia, regione, longitudine, latitudine, nome_stazione FROM temporaneatab GROUP BY nome_stazione ORDER BY nome_stazione asc")
    rows2 = cur.fetchall()
    
    datiGEOJSON.write("{\"type\":\"FeatureCollection\",\"features\":[\n")
    for row2 in rows2:
        datiGEOJSON.write("{\"type\": \"Feature\",\"geometry\":{\"type\": \"Point\",\"coordinates\":["+str(row2[3])+","+str(row2[4])+"]},")
        datiGEOJSON.write("\"properties\":{\"comune\":\""+row2[0]+"\",\"provincia\":\""+row2[1]+"\",\"regione\":\""+row2[2]+"\"}},\n")

    datiGEOJSON.seek(-2,1) #torna indietro di 2 caratteri dalla posizione corrente ed elimina l'ultima virgola
    datiGEOJSON.write("\n]}")
    
comm.close()

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<body>"
if csv:
    print "<a href=\"dati.csv\"><button type=\"button\">CSV</button><br></a>"
if gjson:
    print "<a href=\"dati.geojson\"><button type=\"button\">GeoJson</button></a>"
if not csv and not gjson:
    print "<h1>Non hai selezionato niente!</h1>"
print "</body>"
print "</html>"
print "\n"
