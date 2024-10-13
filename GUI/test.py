import pytest
import sqlite3
from connessione_sqlite import Comunicazione

# Funzione per configurare il database in memoria per ogni test
@pytest.fixture
def db():
    # Creiamo un database temporaneo in memoria
    conn = sqlite3.connect(':memory:')
    
    # Creiamo le tabelle necessarie
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE tabella_dati (
        CODICE TEXT PRIMARY KEY, 
        NOME TEXT, 
        AZIENDA TEXT, 
        PREZZO REAL, 
        SCORTE INTEGER
    )''')
    cursor.execute('''
    CREATE TABLE tabella_clienti (
        CODICE_FISCALE TEXT PRIMARY KEY,
        NOME TEXT,
        COGNOME TEXT,
        TELEFONO TEXT,
        DATA_DI_NASCITA TEXT,
        PRODOTTI_ACQUISTATI INTEGER
    )''')
    cursor.execute('''
    CREATE TABLE tabella_aziende (
        CODICE TEXT PRIMARY KEY,
        NOME TEXT,
        TIPOLOGIA TEXT,
        LOCALIZZAZIONE TEXT,
        RAGIONE_SOCIALE TEXT
    )''')
    
    conn.commit()
    yield conn
    conn.close()  # Chiudiamo la connessione dopo il test

@pytest.fixture
def comunicazione(db):
    # Inizializziamo l'oggetto Comunicazione con il database di test
    com = Comunicazione()
    com.connessione = db  # Usare il db in memoria per i test
    return com

# Test per inserire un prodotto nel database
def test_inserisci_prodotto(comunicazione):
    comunicazione.inserisci_prodotto("123", "ProdottoTest", "AziendaTest", 10.99, 100)
    prodotti = comunicazione.mostra_prodotti()
    assert len(prodotti) == 1
    assert prodotti[0][0] == "123"
    assert prodotti[0][1] == "ProdottoTest"
    assert prodotti[0][2] == "AziendaTest"

# Test per la modifica di un prodotto
def test_modifica_prodotto(comunicazione):
    comunicazione.inserisci_prodotto("123", "ProdottoTest", "AziendaTest", 10.99, 100)
    comunicazione.modifica_prodotti("123", "ProdottoModificato", "AziendaModificata", 15.99, 150)
    prodotti = comunicazione.mostra_prodotti()
    assert prodotti[0][1] == "ProdottoModificato"
    assert prodotti[0][2] == "AziendaModificata"
    assert prodotti[0][3] == 15.99

# Test per eliminare un prodotto dal database
def test_elimina_prodotto(comunicazione):
    comunicazione.inserisci_prodotto("123", "ProdottoTest", "AziendaTest", 10.99, 100)
    comunicazione.elimina_prodotti("ProdottoTest")
    prodotti = comunicazione.mostra_prodotti()
    assert len(prodotti) == 0

# Test per cercare un prodotto nel database
def test_cerca_prodotto(comunicazione):
    comunicazione.inserisci_prodotto("123", "ProdottoTest", "AziendaTest", 10.99, 100)
    prodotto = comunicazione.cerca_prodotto("ProdottoTest")
    assert len(prodotto) == 1
    assert prodotto[0][1] == "ProdottoTest"

# Test per togliere scorte
def test_togli_scorte(comunicazione):
    comunicazione.inserisci_prodotto("123", "ProdottoTest", "AziendaTest", 10.99, 100)
    comunicazione.togli_scorte("123", 50)
    prodotti = comunicazione.mostra_prodotti()
    assert prodotti[0][4] == 50