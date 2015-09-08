#SCRIVE SU FILE
Myfile = open("credenziali.txt","w")
Myfile.write("nico\n12345")
Myfile.close

#LEGGE DA FILE SOLO LINEA PER LINEA
Myfile = open("credenziali.txt","r")
user = Myfile.readline()
pas = Myfile.readline()
print user,pas
Myfile.close