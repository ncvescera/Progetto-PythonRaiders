#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial 

In this example, a QtGui.QCheckBox widget
is used to toggle the title of a window.

author: Jan Bodnar
website: zetcode.com 
last edited: September 2011
"""


import sys
import psycopg2
from PyQt4 import QtGui, QtCore

scriviCSV = 0
scriviGEOJSON = 0

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        button = QtGui.QPushButton('Test', self)
        button.move(170,50)
        
        label = QtGui.QLabel('Seleziona il formato in cui vuoi esportare i dati', self)
        label.move(20,20)
        button.clicked.connect(self.exitNow) 
        
        self.initUI()
        
    def initUI(self):      

        cb = QtGui.QCheckBox('CSV', self)
        cb2 = QtGui.QCheckBox('GEOJSON',self)
        cb.move(20, 50)
        cb2.move(80,50)
        #cb.toggle()
        cb.stateChanged.connect(self.changeValueCSS)
        cb2.stateChanged.connect(self.changeValueGEOJSON)
        
        self.setGeometry(500, 500, 350, 100)
        self.setWindowTitle('Seleziona Formato')
        self.show()
        
        
    def changeValueCSS(self,state):
      
        if state == QtCore.Qt.Checked:
            #self.setWindowTitle('QtGui.QCheckBox')
            global scriviCSV 
            scriviCSV = 1
            print scriviCSV
        else:
            #self.setWindowTitle('')
            scriviCSV = 0
            
    def changeValueGEOJSON(self, state):
        if state == QtCore.Qt.Checked:
            global scriviGEOJSON
            scriviGEOJSON = 1
            print scriviGEOJSON
        else:
            scriviGEOJSON = 0
        
    def exitNow(self):    
        
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
        cur.execute("SELECT comune, provincia, regione, longitudine, latitudine FROM temporaneatab")
        rows = cur.fetchall()

        if scriviCSV == 1:
            datiCSV = open("dati.csv","w")
            print "---Inizio scrittura CSV---"
            for row in rows:
                #print row,"\n"
                datiCSV.write(str(row).strip("()"))
                datiCSV.write("\n")

            print "---Fine scrittura---"
        if scriviGEOJSON == 1:   
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
        
        
        self.close()
        

app = QtGui.QApplication(sys.argv)
ex = Example()
ex.show()
sys.exit(app.exec_())
    



