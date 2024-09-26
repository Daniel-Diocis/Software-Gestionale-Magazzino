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
        self.ui.bt_elimina.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_eliminar))
        self.ui.bt_impostazioni.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_ajustes))

        # Larghezza della colonna adattabile
        self.ui.tabella_elimina.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tabella_prodotti.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

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

if __name__ == "__main__":
     app = QApplication(sys.argv)
     my_app = FinestraPrincipale()
     my_app.show()
     sys.exit(app.exec_())