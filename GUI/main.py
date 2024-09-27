import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtCore import  QPropertyAnimation,QEasingCurve
from PyQt5 import QtCore, QtWidgets
from disegno import Ui_MainWindow
from connessione_sqlite import Comunicazione

class FinestraPrincipale(QMainWindow):
    def __init__(self):
        super(FinestraPrincipale, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.bt_menu.clicked.connect(self.muovi_menu)
        
        self.basedidati = Comunicazione()

        self.ui.bt_minimo.hide()

        self.ui.bt_aggiorna.clicked.connect(self.mostra_prodotti)
        self.ui.bt_aggiungere.clicked.connect(self.registra_prodotti)
        self.ui.bt_eliminare.clicked.connect(self.elimina_prodotti)
        self.ui.bt_modifica_tabella.clicked.connect(self.modifica_prodotti)
        self.ui.bt_mod_cerca.clicked.connect(self.cerca_per_nome_modifica)
        self.ui.bt_eliminare_cerca.clicked.connect(self.cerca_per_nome_elimina)

        self.ui.bt_aggiorna_clienti.clicked.connect(self.mostra_clienti)
        self.ui.bt_reg_registra_cliente.clicked.connect(self.registra_clienti)
        self.ui.bt_eli_eliminare_cliente.clicked.connect(self.elimina_clienti)
        self.ui.bt_mod_modifica_cliente.clicked.connect(self.modifica_clienti)
        self.ui.bt_mod_cerca_cliente.clicked.connect(self.cerca_per_nome_modifica_cliente)
        self.ui.bt_eliminare_cerca_cliente.clicked.connect(self.cerca_per_nome_elimina_cliente)

        self.ui.bt_aggiorna_aziende.clicked.connect(self.mostra_aziende)
        self.ui.bt_reg_aggiungere_azienda.clicked.connect(self.registra_aziende)
        self.ui.bt_eli_eliminare_azienda.clicked.connect(self.elimina_aziende)
        self.ui.bt_mod_modifica_azienda.clicked.connect(self.modifica_aziende)
        self.ui.bt_mod_cerca_azienda.clicked.connect(self.cerca_per_nome_modifica_azienda)
        self.ui.bt_eliminare_azienda.clicked.connect(self.cerca_per_nome_elimina_azienda)

        self.ui.bt_mod_cerca_prodotto_acquista.clicked.connect(self.cerca_per_nome_prodotto_acquista)
        self.ui.bt_mod_cerca_cliente_acquista.clicked.connect(self.cerca_per_nome_cliente_acquista)
        self.ui.bt_acq_acquista.clicked.connect(self.registra_acquisto)

        self.ui.bt_minimizzare.clicked.connect(self.control_bt_minimizzare)
        self.ui.bt_minimo.clicked.connect(self.control_bt_minimo)
        self.ui.bt_massimo.clicked.connect(self.control_bt_massimo)
        self.ui.bt_chiudere.clicked.connect(lambda: self.close())

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        #SizeGrip
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)
        # Posiziona il grip inizialmente
        self.grip.move(self.width() - self.gripSize, self.height() - self.gripSize)

        # mouovi finestra
        self.ui.frame_superior.mouseMoveEvent = self.muovi_finestra

        # connessione bottoni
        self.ui.bt_database.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_database))
        self.ui.bt_registra.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_registra))
        self.ui.bt_modifica.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_modifica))
        self.ui.bt_elimina.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_elimina))
        self.ui.bt_clienti.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_cliente))
        self.ui.bt_aggiungi_cliente.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_aggiungi_cliente))
        self.ui.bt_modifica_cliente.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_modifica_cliente))
        self.ui.bt_elimina_cliente.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_elimina_cliente))
        self.ui.bt_acquista.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_acquista))
        self.ui.bt_aziende.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_aziende))
        self.ui.bt_aggiungi_azienda.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_aggiungi_azienda))
        self.ui.bt_modifica_azienda.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_modifica_azienda))
        self.ui.bt_elimina_azienda.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_elimina_azienda))

        # Larghezza della colonna adattabile
        self.ui.tabella_elimina.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tabella_prodotti.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tabella_elimina_cliente.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tabella_clienti.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tabella_elimina_azienda.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tabella_aziende.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Imposta la pagina Database come pagina
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_database)

    def control_bt_minimizzare(self):
        self.showMinimized()

    def control_bt_minimo(self):
        self.showNormal()
        self.ui.bt_minimo.hide()
        self.ui.bt_massimo.show()

    def  control_bt_massimo(self): 
        self.showMaximized()
        self.ui.bt_massimo.hide()
        self.ui.bt_minimo.show()

    ## SizeGrip
    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    ## muovere finestra
    def mousePressEvent(self, event):
        self.click_position = event.globalPos()

    def muovi_finestra(self, event):
        if self.isMaximized() == False:         
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.click_position)
                self.click_position = event.globalPos()
                event.accept()
        if event.globalPos().y() <=10:
            self.showMaximized()
            self.ui.bt_massimo.hide()
            self.ui.bt_minimo.show()
        else:
            self.showNormal()
            self.ui.bt_minimo.hide()
            self.ui.bt_massimo.show()

    # Metodo para mover el menu lateral izquierdo
    def muovi_menu(self):
        if True:            
            width = self.ui.frame_control.width()
            normal = 0
            if width==0:
                extender = 200
            else:
                extender = normal
            self.animacion = QPropertyAnimation(self.ui.frame_control, b'minimumWidth')
            self.animacion.setDuration(300)
            self.animacion.setStartValue(width)
            self.animacion.setEndValue(extender)
            self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacion.start()

    # Configuracion Pagina Base de datos
    def mostra_prodotti(self):  
        dati = self.basedidati.mostra_prodotti()
        i = len(dati)
        self.ui.tabella_prodotti.setRowCount(i)
        tablerow = 0
        for row in dati:
            self.Id = row[0]
            self.ui.tabella_prodotti.setItem(tablerow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.ui.tabella_prodotti.setItem(tablerow,1,QtWidgets.QTableWidgetItem(str(row[1])))
            self.ui.tabella_prodotti.setItem(tablerow,2,QtWidgets.QTableWidgetItem(str(row[2])))
            self.ui.tabella_prodotti.setItem(tablerow,3,QtWidgets.QTableWidgetItem(str(row[3])))
            self.ui.tabella_prodotti.setItem(tablerow,4,QtWidgets.QTableWidgetItem(str(row[4])))
            tablerow +=1
            self.ui.signal_modifica.setText("")
            self.ui.signal_registra.setText("")
            self.ui.signal_elimina.setText("")

    def registra_prodotti(self):
        codice = self.ui.reg_codice.text().upper()  
        nome = self.ui.reg_nome.text().upper() 
        azienda = self.ui.reg_azienda.text().upper() 
        prezzo = self.ui.reg_prezzo.text().upper() 
        scorte = self.ui.reg_scorte.text().upper() 
        if codice != '' and nome != '' and azienda != '' and prezzo != '' and scorte !='':
            self.basedidati.inserisci_prodotto(codice, nome, azienda, prezzo, scorte)
            self.ui.signal_registra.setText('Prodotti Registrati')
            self.ui.reg_codice.clear()
            self.ui.reg_nome.clear()
            self.ui.reg_azienda.clear()
            self.ui.reg_prezzo.clear()
            self.ui.reg_scorte.clear()
        else:
            self.ui.signal_registra.setText('Ci sono spazi vuoti')
    
    def cerca_per_nome_modifica(self):
        codice_prodotto = self.ui.mod_cerca.text().upper() 
        codice_prodotto = str("'" + codice_prodotto + "'")
        self.prodotto = self.basedidati.cerca_prodotto(codice_prodotto)
        if len(self.prodotto) !=0:
            self.ui.mod_codice.setText(str(self.prodotto[0][0]))
            self.ui.mod_nome.setText(str(self.prodotto[0][1]))
            self.ui.mod_azienda.setText(str(self.prodotto[0][2]))
            self.ui.mod_prezzo.setText(str(self.prodotto[0][3]))
            self.ui.mod_scorte.setText(str(self.prodotto[0][4]))
        else:
            self.ui.signal_modifica.setText("NON ESISTE")

    def modifica_prodotti(self):
        if self.prodotto != '':
            codice = self.ui.mod_codice.text().upper()  
            nome = self.ui.mod_nome.text().upper() 
            azienda = self.ui.mod_azienda.text().upper() 
            prezzo = self.ui.mod_prezzo.text().upper() 
            scorte = self.ui.mod_scorte.text().upper() 
            mod = self.basedidati.modifica_prodotti(codice, nome, azienda, prezzo, scorte)
            if mod == 1:
                self.ui.signal_modifica.setText("MODIFICATO")                
                self.ui.mod_codice.clear()
                self.ui.mod_nome.clear()
                self.ui.mod_azienda.clear()
                self.ui.mod_prezzo.clear()                
                self.ui.mod_scorte.clear()
                self.ui.mod_cerca.setText('')
            elif mod == 0:
                self.ui.signal_modifica.setText("ERRORE")
            else:
                self.ui.signal_modifica.setText("SBAGLIATO")

    def cerca_per_nome_elimina(self):
        nome_prodotto = self.ui.eliminare_cerca.text().upper()
        nome_prodotto = str("'" + nome_prodotto + "'")
        prodotto = self.basedidati.cerca_prodotto(nome_prodotto)
        self.ui.tabella_elimina.setRowCount(len(prodotto))

        if len(prodotto) == 0:
            self.ui.signal_elimina.setText(' Non Esiste')       
        else:
            self.ui.signal_elimina.setText('Prodotto Selezionato')
        tablerow = 0
        for row in prodotto:
            self.prodotto_da_eliminare = row[1]
            self.ui.tabella_elimina.setItem(tablerow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.ui.tabella_elimina.setItem(tablerow,1,QtWidgets.QTableWidgetItem(str(row[1])))
            self.ui.tabella_elimina.setItem(tablerow,2,QtWidgets.QTableWidgetItem(str(row[2])))
            self.ui.tabella_elimina.setItem(tablerow,3,QtWidgets.QTableWidgetItem(str(row[3])))
            self.ui.tabella_elimina.setItem(tablerow,4,QtWidgets.QTableWidgetItem(str(row[4])))
            tablerow +=1

    def elimina_prodotti(self):
        self.row_flag = self.ui.tabella_elimina.currentRow()
        if self.row_flag == 0:
            self.ui.tabella_elimina.removeRow(0)
            self.basedidati.elimina_prodotti("'" + self.prodotto_da_eliminare + "'")
            self.ui.signal_elimina.setText('Prodotto Eliminato')
            self.ui.eliminare_cerca.setText('')

    def mostra_clienti(self):  
        clienti = self.basedidati.mostra_clienti()
        i = len(clienti)
        self.ui.tabella_clienti.setRowCount(i)
        tablerow = 0
        for row in clienti:
            self.Id = row[0]
            self.ui.tabella_clienti.setItem(tablerow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.ui.tabella_clienti.setItem(tablerow,1,QtWidgets.QTableWidgetItem(str(row[1])))
            self.ui.tabella_clienti.setItem(tablerow,2,QtWidgets.QTableWidgetItem(str(row[2])))
            self.ui.tabella_clienti.setItem(tablerow,3,QtWidgets.QTableWidgetItem(str(row[3])))
            self.ui.tabella_clienti.setItem(tablerow,4,QtWidgets.QTableWidgetItem(str(row[4])))
            self.ui.tabella_clienti.setItem(tablerow,5,QtWidgets.QTableWidgetItem(str(row[5])))
            tablerow +=1
            self.ui.signal_modifica_cliente.setText("")
            self.ui.signal_registra_cliente.setText("")
            self.ui.signal_elimina_cliente.setText("")

    def registra_clienti(self):
        codiceFiscale = self.ui.reg_codiceFiscale_cliente.text().upper()  
        nome = self.ui.reg_nome_cliente.text().upper() 
        cognome = self.ui.reg_cognome_cliente.text().upper() 
        telefono = self.ui.reg_telefono_cliente.text().upper() 
        dataDiNascita = self.ui.reg_dataDiNascitaCliente.text().upper()
        prodottiAcquistati = 0
        if codiceFiscale != '' and nome != '' and cognome != '' and telefono != '' and dataDiNascita != '' and prodottiAcquistati != '':
            self.basedidati.inserisci_cliente(codiceFiscale, nome, cognome, telefono, dataDiNascita, prodottiAcquistati)
            self.ui.signal_registra_cliente.setText('Clienti Registrati')
            self.ui.reg_codiceFiscale_cliente.clear()
            self.ui.reg_nome_cliente.clear()
            self.ui.reg_cognome_cliente.clear()
            self.ui.reg_telefono_cliente.clear()
            self.ui.reg_dataDiNascitaCliente.clear()
        else:
            self.ui.signal_registra_cliente.setText('Ci sono spazi vuoti')

    def cerca_per_nome_modifica_cliente(self):
        codiceFiscale_cliente = self.ui.mod_cerca_cliente.text().upper() 
        codiceFiscale_cliente = str("'" + codiceFiscale_cliente + "'")
        self.cliente = self.basedidati.cerca_cliente(codiceFiscale_cliente)
        if len(self.cliente) !=0:
            self.ui.mod_codFiscale_cliente.setText(str(self.cliente[0][0]))
            self.ui.mod_nome_cliente.setText(str(self.cliente[0][1]))
            self.ui.mod_cognome_cliente.setText(str(self.cliente[0][2]))
            self.ui.mod_telefono_cliente.setText(str(self.cliente[0][3]))
            self.ui.mod_dataDiNascita_cliente.setText(str(self.cliente[0][4]))
        else:
            self.ui.signal_modifica_cliente.setText("NON ESISTE")

    def modifica_clienti(self):
        if self.cliente != '':
            codiceFiscale = self.ui.mod_codFiscale_cliente.text().upper()  
            nome = self.ui.mod_nome_cliente.text().upper() 
            cognome = self.ui.mod_cognome_cliente.text().upper() 
            telefono = self.ui.mod_telefono_cliente.text().upper() 
            dataDiNascita = self.ui.mod_dataDiNascita_cliente.text().upper()
            mod = self.basedidati.modifica_clienti(codiceFiscale, nome, cognome, telefono, dataDiNascita)
            if mod == 1:
                self.ui.signal_modifica_cliente.setText("MODIFICATO")                
                self.ui.mod_codFiscale_cliente.clear()
                self.ui.mod_nome_cliente.clear()
                self.ui.mod_cognome_cliente.clear()
                self.ui.mod_telefono_cliente.clear()                
                self.ui.mod_dataDiNascita_cliente.clear()
                self.ui.mod_cerca_cliente.setText('')
            elif mod == 0:
                self.ui.signal_modifica_cliente.setText("ERRORE")
            else:
                self.ui.signal_modifica_cliente.setText("SBAGLIATO")

    def cerca_per_nome_elimina_cliente(self):
        nome_cliente = self.ui.eliminare_cerca_2.text().upper()
        nome_cliente = str("'" + nome_cliente + "'")
        cliente = self.basedidati.cerca_cliente(nome_cliente)
        print(cliente)
        self.ui.tabella_elimina_cliente.setRowCount(len(cliente))

        if len(cliente) == 0:
            self.ui.signal_elimina_cliente.setText(' Non Esiste')       
        else:
            self.ui.signal_elimina_cliente.setText('Cliente Selezionato')
        tablerow = 0
        for row in cliente:
            self.cliente_da_eliminare = row[1]
            self.ui.tabella_elimina_cliente.setItem(tablerow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.ui.tabella_elimina_cliente.setItem(tablerow,1,QtWidgets.QTableWidgetItem(str(row[1])))
            self.ui.tabella_elimina_cliente.setItem(tablerow,2,QtWidgets.QTableWidgetItem(str(row[2])))
            self.ui.tabella_elimina_cliente.setItem(tablerow,3,QtWidgets.QTableWidgetItem(str(row[3])))
            self.ui.tabella_elimina_cliente.setItem(tablerow,4,QtWidgets.QTableWidgetItem(str(row[4])))
            self.ui.tabella_elimina_cliente.setItem(tablerow,5,QtWidgets.QTableWidgetItem(str(row[5])))
            tablerow +=1

    def elimina_clienti(self):
        self.row_flag = self.ui.tabella_elimina_cliente.currentRow()
        if self.row_flag == 0:
            self.ui.tabella_elimina_cliente.removeRow(0)
            self.basedidati.elimina_clienti("'" + self.cliente_da_eliminare + "'")
            self.ui.signal_elimina_cliente.setText('Cliente Eliminato')
            self.ui.bt_eliminare_cerca_cliente.setText('')

    def cerca_per_nome_prodotto_acquista(self):
        codice_prodotto = self.ui.mod_cerca_prodotto_acquista.text().upper() 
        codice_prodotto = str("'" + codice_prodotto + "'")
        self.prodotto = self.basedidati.cerca_prodotto(codice_prodotto)
        if len(self.prodotto) !=0:
            self.ui.label_codiceProdotto_acquista.setText(str(self.prodotto[0][0]))
            self.ui.label_nomeProdotto_acquista.setText(str(self.prodotto[0][1]))
            self.ui.label_acqiendaProdotto_acquista.setText(str(self.prodotto[0][2]))
            self.ui.label_prezzoProdotto_acquista.setText(str(self.prodotto[0][3]))
            self.ui.label_scorteProdotto_acquista.setText(str(self.prodotto[0][4]))
        else:
            self.ui.signal_registra_acquista.setText("NON ESISTE")

    def cerca_per_nome_cliente_acquista(self):
        codiceFiscale_cliente = self.ui.mod_cerca_cliente_acquista.text().upper() 
        codiceFiscale_cliente = str("'" + codiceFiscale_cliente + "'")
        self.cliente = self.basedidati.cerca_cliente(codiceFiscale_cliente)
        if len(self.cliente) !=0:
            self.ui.label_codiceFiscaleCliente_acquista.setText(str(self.cliente[0][0]))
            self.ui.label_nomeCliente_acquista.setText(str(self.cliente[0][1]))
            self.ui.label_cognomeCliente_acquista.setText(str(self.cliente[0][2]))
            self.ui.label_dataDiNascitaCliente_acquista.setText(str(self.cliente[0][3]))
            self.ui.label_prodottiAcquistatiCliente_acquista.setText(str(self.cliente[0][5]))
        else:
            self.ui.signal_registra_acquista.setText("NON ESISTE")

    def registra_acquisto(self):
        nuove_scorte = int(self.ui.label_scorteProdotto_acquista.text())
        scorteVenduteOra = int(self.ui.spinBox_quantita_acquista.text())
        codice = self.ui.label_codiceProdotto_acquista.text()
        nuove_scorte -= scorteVenduteOra
        modScorte = self.basedidati.togli_scorte(codice, nuove_scorte)
        nuovi_prodottiAcquistati = int(self.ui.label_prodottiAcquistatiCliente_acquista.text())
        nuovi_prodottiAcquistati += scorteVenduteOra
        codiceFiscale = self.ui.label_codiceFiscaleCliente_acquista.text()
        modProdottiAcquistati = self.basedidati.aggiungi_prodotti(codiceFiscale, nuovi_prodottiAcquistati)
        
        if modScorte == 1 and modProdottiAcquistati == 1:
            self.ui.signal_registra_acquista.setText("ACQUISTATO")                
            self.ui.label_codiceProdotto_acquista.clear()
            self.ui.label_nomeProdotto_acquista.clear()
            self.ui.label_acqiendaProdotto_acquista.clear()
            self.ui.label_prezzoProdotto_acquista.clear()                
            self.ui.label_scorteProdotto_acquista.clear()
            self.ui.mod_cerca_prodotto_acquista.setText('')
            self.ui.label_codiceFiscaleCliente_acquista.clear()
            self.ui.label_nomeCliente_acquista.clear()
            self.ui.label_cognomeCliente_acquista.clear()
            self.ui.label_dataDiNascitaCliente_acquista.clear()
            self.ui.label_prodottiAcquistatiCliente_acquista.clear()
            self.ui.mod_cerca_cliente_acquista.setText('')
        elif modScorte == 0 and modProdottiAcquistati == 0:
            self.ui.signal_registra_acquista.setText("ERRORE")
        else:
            self.ui.signal_registra_acquista.setText("SBAGLIATO")

    def mostra_aziende(self):  
        aziende = self.basedidati.mostra_aziende()
        i = len(aziende)
        self.ui.tabella_aziende.setRowCount(i)
        tablerow = 0
        for row in aziende:
            self.Id = row[0]
            self.ui.tabella_aziende.setItem(tablerow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.ui.tabella_aziende.setItem(tablerow,1,QtWidgets.QTableWidgetItem(str(row[1])))
            self.ui.tabella_aziende.setItem(tablerow,2,QtWidgets.QTableWidgetItem(str(row[2])))
            self.ui.tabella_aziende.setItem(tablerow,3,QtWidgets.QTableWidgetItem(str(row[3])))
            self.ui.tabella_aziende.setItem(tablerow,4,QtWidgets.QTableWidgetItem(str(row[4])))
            tablerow +=1
            self.ui.signal_modifica_azienda.setText("")
            self.ui.signal_registra_azienda.setText("")
            self.ui.signal_elimina_azienda.setText("")

    def registra_aziende(self):
        codice = self.ui.reg_codice_azienda.text().upper()  
        nome = self.ui.reg_nome_azienda.text().upper() 
        tipologia = self.ui.reg_tipologia_azienda.text().upper() 
        localizzazione = self.ui.reg_localizzazione_azienda.text().upper() 
        ragioneSociale = self.ui.reg_ragioneSociale_azienda.text().upper()
        if codice != '' and nome != '' and tipologia != '' and localizzazione != '' and ragioneSociale != '':
            self.basedidati.inserisci_aziende(codice, nome, tipologia, localizzazione, ragioneSociale)
            self.ui.signal_registra_azienda.setText('Azienda Registrata')
            self.ui.reg_codice_azienda.clear()
            self.ui.reg_nome_azienda.clear()
            self.ui.reg_tipologia_azienda.clear()
            self.ui.reg_localizzazione_azienda.clear()
            self.ui.reg_ragioneSociale_azienda.clear()
        else:
            self.ui.signal_registra_azienda.setText('Ci sono spazi vuoti')

    def cerca_per_nome_modifica_azienda(self):
        codice_azienda = self.ui.mod_cerca_azienda.text().upper() 
        codice_azienda = str("'" + codice_azienda + "'")
        self.azienda = self.basedidati.cerca_azienda(codice_azienda)
        if len(self.azienda) !=0:
            self.ui.mod_codice_azienda.setText(str(self.azienda[0][0]))
            self.ui.mod_nome_azienda.setText(str(self.azienda[0][1]))
            self.ui.mod_tipologia_azienda.setText(str(self.azienda[0][2]))
            self.ui.mod_localizzazione_azienda.setText(str(self.azienda[0][3]))
            self.ui.mod_ragioneSociale_azienda.setText(str(self.azienda[0][4]))
        else:
            self.ui.signal_modifica_azienda.setText("NON ESISTE")

    def modifica_aziende(self):
        if self.azienda != '':
            codice = self.ui.mod_codice_azienda.text().upper()  
            nome = self.ui.mod_nome_azienda.text().upper() 
            tipologia = self.ui.mod_tipologia_azienda.text().upper() 
            localizzazione = self.ui.mod_localizzazione_azienda.text().upper() 
            ragioneSociale = self.ui.mod_ragioneSociale_azienda.text().upper()
            mod = self.basedidati.modifica_aziende(codice, nome, tipologia, localizzazione, ragioneSociale)
            if mod == 1:
                self.ui.signal_modifica_azienda.setText("MODIFICATO")                
                self.ui.mod_codice_azienda.clear()
                self.ui.mod_nome_azienda.clear()
                self.ui.mod_tipologia_azienda.clear()
                self.ui.mod_localizzazione_azienda.clear()                
                self.ui.mod_ragioneSociale_azienda.clear()
                self.ui.mod_cerca_azienda.setText('')
            elif mod == 0:
                self.ui.signal_modifica_azienda.setText("ERRORE")
            else:
                self.ui.signal_modifica_azienda.setText("SBAGLIATO")

    def cerca_per_nome_elimina_azienda(self):
        nome_azienda = self.ui.eliminare_cerca_azienda.text().upper()
        nome_azienda = str("'" + nome_azienda + "'")
        azienda = self.basedidati.cerca_azienda(nome_azienda)
        self.ui.tabella_elimina_azienda.setRowCount(len(azienda))

        if len(azienda) == 0:
            self.ui.signal_elimina_azienda.setText(' Non Esiste')       
        else:
            self.ui.signal_elimina_azienda.setText('Azienda Selezionata')
        tablerow = 0
        for row in azienda:
            self.azienda_da_eliminare = row[1]
            self.ui.tabella_elimina_azienda.setItem(tablerow,0,QtWidgets.QTableWidgetItem(str(row[0])))
            self.ui.tabella_elimina_azienda.setItem(tablerow,1,QtWidgets.QTableWidgetItem(str(row[1])))
            self.ui.tabella_elimina_azienda.setItem(tablerow,2,QtWidgets.QTableWidgetItem(str(row[2])))
            self.ui.tabella_elimina_azienda.setItem(tablerow,3,QtWidgets.QTableWidgetItem(str(row[3])))
            self.ui.tabella_elimina_azienda.setItem(tablerow,4,QtWidgets.QTableWidgetItem(str(row[4])))
            tablerow +=1

    def elimina_aziende(self):
        self.row_flag = self.ui.tabella_elimina_azienda.currentRow()
        if self.row_flag == 0:
            self.ui.tabella_elimina_azienda.removeRow(0)
            self.basedidati.elimina_aziende("'" + self.azienda_da_eliminare + "'")
            self.ui.signal_elimina_azienda.setText('Azienda Eliminata')
            self.ui.bt_eli_eliminare_azienda.setText('')

if __name__ == "__main__":
     app = QApplication(sys.argv)
     my_app = FinestraPrincipale()
     my_app.show()
     sys.exit(app.exec_())