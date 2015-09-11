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
cur.execute("SELECT nome_stazione, min(comune) as comune, min(provincia) as provincia, min(regione) as regione, min(longitudine) as longitudine, min(latitudine) as latitudine FROM temporaneatab GROUP BY nome_stazione ORDER BY nome_stazione asc")
rows = cur.fetchall()

csv = form.getvalue('CSV')

if csv:
    datiCSV = ""
    for row in rows:
        datiCSV = str(datiCSV)+str(row).strip("()").replace(",",";")+"\n"

gjson = form.getvalue('geoJson')       
if gjson:
    datiGEOJSON = ""
    cur = comm.cursor()
    cur.execute("SELECT nome_stazione, min(comune) as comune, min(provincia) as provincia, min(regione) as regione, min(longitudine) as longitudine, min(latitudine) as latitudine FROM temporaneatab GROUP BY nome_stazione ORDER BY nome_stazione asc")
    righe = cur.fetchall()

    ctrl=0
    
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

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<link rel=\"stylesheet\"href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css\">"
print "<link rel=\"stylesheet\"href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css\">"
print "</head>"
print "<body>"
if csv:
    print "<a href=\"dati.csv\"><button type=\"button\">CSV</button><br></a>"
if gjson:
    print "<a href=\"dati.geojson\"><button type=\"button\" class=\"btn btn-primary btn-lg btn-block\">GeoJson</button></a>"
if not csv and not gjson:
    print "<h1>Non hai selezionato niente!</h1>"
print "</body>"
print "</html>"
print "\n"
