import sqlite3

class Comunicazione():
    def __init__(self):
        self.connessione = sqlite3.connect('../basedidati.db')

    def inserisci_prodotto(self, codice, nome, azienda, prezzo, scorte):
        cursor = self.connessione.cursor()
        bd = '''INSERT INTO tabella_dati (CODICE, NOME, AZIENDA, PREZZO, SCORTE)
                VALUES (?, ?, ?, ?, ?)''' 
        
        cursor.execute(bd, (codice, nome, azienda, prezzo, scorte))  # Passa i valori come tupla
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
        bd = '''SELECT * FROM tabella_dati WHERE NOME = ?'''
        cursor.execute(bd, (nome_prodotto,))  
        risultati = cursor.fetchall()  # Recupera tutti i risultati
        cursor.close()
        return risultati
    
    def elimina_prodotti(self, nome):
        cursor = self.connessione.cursor()
        bd = '''DELETE FROM tabella_dati WHERE NOME = ?'''
        cursor.execute(bd, (nome,))  # Passa il nome come una tupla
        self.connessione.commit()
        cursor.close()

    def modifica_prodotti(self, codice, nome, azienda, prezzo, scorte):
        cursor = self.connessione.cursor()
        bd = '''UPDATE tabella_dati 
                SET NOME = ?, AZIENDA = ?, PREZZO = ?, SCORTE = ? 
                WHERE CODICE = ?'''
        # Passa i valori come tupla
        cursor.execute(bd, (nome, azienda, prezzo, scorte, codice))
    
        a = cursor.rowcount  # Ottieni il numero di righe modificate
        self.connessione.commit()
        cursor.close()
        return a
    
    def inserisci_cliente(self, codiceFiscale, nome, cognome, telefono, dataDiNascita, prodottiAcquistati):
        cursor = self.connessione.cursor()
        bd = '''INSERT INTO tabella_clienti (CODICE_FISCALE, NOME, COGNOME, TELEFONO, DATA_DI_NASCITA, PRODOTTI_ACQUISTATI)
                VALUES (?, ?, ?, ?, ?, ?)''' 
        
        cursor.execute(bd, (codiceFiscale, nome, cognome, telefono, dataDiNascita, 0))  # Passa i valori come tupla
        self.connessione.commit()
        cursor.close()

    def mostra_clienti(self):
        cursor = self.connessione.cursor()
        bd = "SELECT * FROM tabella_clienti"
        cursor.execute(bd)
        registro = cursor.fetchall()
        return registro
    
    def cerca_cliente(self, nome_cliente):
        cursor = self.connessione.cursor()
        bd = '''SELECT * FROM tabella_clienti WHERE NOME = ?'''
        cursor.execute(bd, (nome_cliente,))
        return cursor.fetchall()
    
    def elimina_clienti(self, nome_cliente):
        cursor = self.connessione.cursor()
        bd = '''DELETE FROM tabella_clienti WHERE NOME = ?'''
        cursor.execute(bd, (nome_cliente,))
        self.connessione.commit()

    def modifica_clienti(self, codiceFiscale, nome, cognome, telefono, dataDiNascita):
        cursor = self.connessione.cursor()
        bd = '''UPDATE tabella_clienti 
                SET NOME = ?, COGNOME = ?, TELEFONO = ?, DATA_DI_NASCITA = ?
                WHERE CODICE_FISCALE = ?'''
        
        cursor.execute(bd, (nome, cognome, telefono, dataDiNascita, codiceFiscale))  # Passa i valori come tupla
        a = cursor.rowcount
        self.connessione.commit()
        cursor.close()
        return a
    
    def togli_scorte(self, codice, nuove_scorte):
        cursor = self.connessione.cursor()
        bd = '''UPDATE tabella_dati 
                SET SCORTE = ? 
                WHERE CODICE = ?'''  
        
        cursor.execute(bd, (nuove_scorte, codice))  
        a = cursor.rowcount
        self.connessione.commit()
        cursor.close()
        return a
    
    def aggiungi_prodotti(self, codiceFiscale, nuovi_prodottiAcquistati):
        cursor = self.connessione.cursor()
        bd = '''UPDATE tabella_clienti SET PRODOTTI_ACQUISTATI = ?
        WHERE CODICE_FISCALE = ?'''
        
        cursor.execute(bd, (nuovi_prodottiAcquistati, codiceFiscale))
        self.connessione.commit()
        
        return cursor.rowcount  # Restituisci il numero di righe modificate
    
    def inserisci_aziende(self, codice, nome, tipologia, localizzazione, ragioneSociale):
        cursor = self.connessione.cursor()
        bd = '''INSERT INTO tabella_aziende (CODICE, NOME, TIPOLOGIA, LOCALIZZAZIONE, RAGIONE_SOCIALE)
                VALUES (?, ?, ?, ?, ?)'''
        
        cursor.execute(bd, (codice, nome, tipologia, localizzazione, ragioneSociale))  # Passa i valori come tupla
        self.connessione.commit()
        cursor.close()

    def mostra_aziende(self):
        cursor = self.connessione.cursor()
        bd = "SELECT * FROM tabella_aziende"
        cursor.execute(bd)
        registro = cursor.fetchall()
        return registro
    
    def cerca_azienda(self, nome):
        cursor = self.connessione.cursor()
        bd = '''SELECT * FROM tabella_aziende WHERE NOME = ?'''
        cursor.execute(bd, (nome,))
        return cursor.fetchall()
    
    def elimina_aziende(self, nome):
        cursor = self.connessione.cursor()
        bd = '''DELETE FROM tabella_aziende WHERE NOME = ?'''
        cursor.execute(bd, (nome,))
        self.connessione.commit()

    def modifica_aziende(self, codice, nome, tipologia, localizzazione, ragioneSociale):
        cursor = self.connessione.cursor()
        bd = '''UPDATE tabella_aziende 
                SET CODICE = ?, NOME = ?, TIPOLOGIA = ?, LOCALIZZAZIONE = ?, RAGIONE_SOCIALE = ?
                WHERE CODICE = ?'''
        cursor.execute(bd, (codice, nome, tipologia, localizzazione, ragioneSociale, codice))  # Passa i valori come tupla
        a = cursor.rowcount
        self.connessione.commit()
        cursor.close()
        return a