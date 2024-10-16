import pytest
import sqlite3
from connessione_sqlite import Comunicazione

@pytest.fixture
def db():
    conn = sqlite3.connect(':memory:')
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
    conn.close()

@pytest.fixture
def comunicazione(db):
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

# Test per la modifica di un prodotto
def test_modifica_prodotto(comunicazione):
    comunicazione.inserisci_prodotto("123", "ProdottoTest", "AziendaTest", 10.99, 100)
    comunicazione.modifica_prodotti("123", "ProdottoModificato", "AziendaModificata", 15.99, 150)
    prodotti = comunicazione.mostra_prodotti()
    assert prodotti[0][1] == "ProdottoModificato"

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

# Test per inserire un cliente
def test_inserisci_cliente(comunicazione):
    comunicazione.inserisci_cliente("ABC123", "NomeTest", "CognomeTest", "1234567890", "01-01-2000", 0)
    clienti = comunicazione.mostra_clienti()
    assert len(clienti) == 1
    assert clienti[0][0] == "ABC123"
    assert clienti[0][5] == 0  # Assicuriamoci che prodotti acquistati siano inizializzati a 0

# Test per modificare un cliente
def test_modifica_cliente(comunicazione):
    comunicazione.inserisci_cliente("ABC123", "NomeTest", "CognomeTest", "1234567890", "01-01-2000", 0)
    comunicazione.modifica_clienti("ABC123", "NuovoNome", "CognomeModificato", "0987654321", "02-02-2000")
    clienti = comunicazione.mostra_clienti()
    assert clienti[0][1] == "NuovoNome"

# Test per eliminare un cliente
def test_elimina_cliente(comunicazione):
    comunicazione.inserisci_cliente("ABC123", "NomeTest", "CognomeTest", "1234567890", "01-01-2000", 0)
    comunicazione.elimina_clienti("NomeTest")
    clienti = comunicazione.mostra_clienti()
    assert len(clienti) == 0

# Test per cercare un cliente
def test_cerca_cliente(comunicazione):
    comunicazione.inserisci_cliente("ABC123", "NomeTest", "CognomeTest", "1234567890", "01-01-2000", 0)
    cliente = comunicazione.cerca_cliente("NomeTest")
    assert len(cliente) == 1
    assert cliente[0][1] == "NomeTest"

# Test per aggiungere prodotti acquistati a un cliente
def test_aggiungi_prodotti(comunicazione):
    comunicazione.inserisci_cliente("ABC123", "NomeTest", "CognomeTest", "1234567890", "01-01-2000", 0)
    comunicazione.aggiungi_prodotti("ABC123", 5)  # Aggiungiamo 5 prodotti acquistati
    cliente = comunicazione.mostra_clienti()
    assert cliente[0][5] == 5  # Verifica che il numero di prodotti acquistati sia ora 5

# Test per inserire un'azienda
def test_inserisci_azienda(comunicazione):
    comunicazione.inserisci_aziende("XYZ123", "AziendaTest", "TipologiaTest", "LocalizzazioneTest", "RagioneSocialeTest")
    aziende = comunicazione.mostra_aziende()
    assert len(aziende) == 1
    assert aziende[0][0] == "XYZ123"

# Test per modificare un'azienda
def test_modifica_azienda(comunicazione):
    comunicazione.inserisci_aziende("XYZ123", "AziendaTest", "TipologiaTest", "LocalizzazioneTest", "RagioneSocialeTest")
    comunicazione.modifica_aziende("XYZ123", "NuovaAzienda", "NuovaTipologia", "NuovaLocalizzazione", "NuovaRagione")
    aziende = comunicazione.mostra_aziende()
    assert aziende[0][1] == "NuovaAzienda"

# Test per eliminare un'azienda
def test_elimina_azienda(comunicazione):
    comunicazione.inserisci_aziende("XYZ123", "AziendaTest", "TipologiaTest", "LocalizzazioneTest", "RagioneSocialeTest")
    comunicazione.elimina_aziende("AziendaTest")
    aziende = comunicazione.mostra_aziende()
    assert len(aziende) == 0

# Test per cercare un'azienda
def test_cerca_azienda(comunicazione):
    comunicazione.inserisci_aziende("XYZ123", "AziendaTest", "TipologiaTest", "LocalizzazioneTest", "RagioneSocialeTest")
    azienda = comunicazione.cerca_azienda("AziendaTest")
    assert len(azienda) == 1
    assert azienda[0][1] == "AziendaTest"