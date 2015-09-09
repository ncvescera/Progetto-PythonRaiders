import psycopg2

scriviCSV = 0

#LEGGE DA FILE SOLO LINEA PER LINEA
Myfile = open("credenziali.txt","r")
dbname= Myfile.readline()
dbname = dbname[:-1] #serve per eliminare l'ultimo carattere: \n
host = Myfile.readline()
host = host[:-1]
user = Myfile.readline()
user = user[:-1]
pas = Myfile.readline()
#print dbname,host,user,pas
Myfile.close

try:
    comm = psycopg2.connect(database = dbname, host = host, user = user, password = pas)
    print "Connessione stabilita con successo :D"
except:
    print "Errore! Impossibile connetersi al Database."
    
#SELECT per selezionare un campo della tabella specificata dopo FROM    
cur = comm.cursor()
cur.execute("SELECT * FROM temporaneatab")
rows = cur.fetchall()

if scriviCSV == 1:
    datiCSV = open("dati.csv","w")
    print "---Inizio scrittura CSV---"
    for row in rows:
        #print row,"\n"
        datiCSV.write(str(row).strip("()"))
        datiCSV.write("\n")
        
    print "---Fine scrittura---"
else:   
    datiGEOJSON = open("dati.geojson","w")  
    cur = comm.cursor()
    cur.execute("SELECT comune, provincia, regione, longitudine, latitudine FROM temporaneatab")
    rows2 = cur.fetchall()
    
    print "---Inizio scrittura GeoJson---"
    datiGEOJSON.write("{\"type\":\"FeatureCollection\",\"features\":[\n")
    for row2 in rows2:
        datiGEOJSON.write("{\"type\": \"Feature\",\"geometry\":{\"type\": \"Point\",\"coordinates\":["+str(row2[3])+","+str(row2[4])+"]},")
        datiGEOJSON.write("\"properties\":{\"comune\":\""+row2[0]+"\",\"provincia\":\""+row2[1]+"\",\"regione\":\""+row2[2]+"\"}},\n")

    datiGEOJSON.seek(-2,1) #torna indietro di 2 caratteri dalla posizione corrente ed elimina l'ultima virgola
    datiGEOJSON.write(" \n]}")
    
print "---Fine Scrittura---"

try:
    comm.close()
    print "---Connessione Terminata---"
except:
    print "Impossibile terminare la connessione!"