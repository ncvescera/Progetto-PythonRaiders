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
#print dbname,host,user,pas
Myfile.close

try:
    comm = psycopg2.connect(database = dbname, host = host, user = user, password = pas)
    print "Connessione stabilita con successo :D"
except:
    print "Errore! Impossibile connetersi al Database."