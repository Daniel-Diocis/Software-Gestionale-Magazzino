import sqlite3

class Comunicazione():
    def __init__(self):
        self.connessione = sqlite3.connect('basedidati.db')

    def inserisci_prodotto(self, codice, nome, azienda, prezzo, scorte):
        cursor = self.connessione.cursor()
        bd = '''INSERT INTO tabella_dati (CODICE, NOME, AZIENDA, PREZZO, SCORTE)
        VALUES('{}','{}','{}','{}','{}')'''.format(codice, nome, azienda, prezzo, scorte)
        cursor.execute(bd)
        self.connessione.commit()
        cursor.close()

    def mostra_prodotti(self):
        cursor = self.connessione.cursor()
        bd = "SELECT * FROM tabella_dati"
        cursor.execute(bd)
        registro = cursor.fetchall()
        return registro
    
    def cerca_prodotto(self, nome_prodotto):
        cursor = self.connessione.cursor()
        bd = '''SELECT * FROM tabella_dati WHERE NOME = {}'''.format(nome_prodotto)
        cursor.execute(bd)
        nomeX = cursor.fetchall()
        cursor.close()
        return nomeX
    
    def elimina_prodotti(self, nome):
        cursor = self.connessione.cursor()
        bd = '''DELETE FROM tabella_dati WHERE NOME = {}'''.format(nome)
        cursor.execute(bd)
        self.connessione.commit()
        cursor.close()

    def modifica_prodotti(self, codice, nome, azienda, prezzo, scorte):
        cursor = self.connessione.cursor()
        bd = '''UPDATE tabella_dati SET CODICE ='{}', NOME = '{}' , AZIENDA = '{}', PREZZO = '{}', SCORTE = '{}'
        WHERE CODICE = '{}' '''.format(codice, nome, azienda, prezzo, scorte, codice)
        print(bd)
        cursor.execute(bd)
        a = cursor.rowcount
        self.connessione.commit()
        cursor.close()
        return a