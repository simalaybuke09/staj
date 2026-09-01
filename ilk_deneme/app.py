from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGroupBox, QLabel, QLineEdit, QSpinBox, 
                             QPushButton, QTabWidget, QTextEdit, QComboBox, QStackedWidget, QMessageBox)
from PyQt6.QtCore import QSize, Qt
import sys
from PLC import PLC
from read_app import readApp
from connect_app import ConnectApp



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.plc = None
        self.initUI()

    def initUI(self):    
        self.setWindowTitle("Siemens PLC Kontrol Paneli")
        self.resize(800, 700)
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        main_layout.addWidget(self.setup_connection_group())
        main_layout.addWidget(self.setup_read_group())
        


    



    def setup_connection_group(self):
        #PLC Bağlantısı 
        conn_group = QGroupBox("Bağlantı Ayarları")
        conn_layout = QHBoxLayout(conn_group)

        self.connection=ConnectApp(self)
        conn_layout.addWidget(self.connection)
        return conn_group






    def setup_read_group(self):
        read_group=QGroupBox("PLC'den Veri Okuma")  
        read_layout=QVBoxLayout(read_group)
        self.tabs = QTabWidget()

        self.tabs.addTab(readApp(self, "Giriş"), "Giriş")
        self.tabs.addTab(readApp(self, "Çıkış"), "Çıkış")
        self.tabs.addTab(readApp(self, "Marker"), "Marker")
        self.tabs.addTab(readApp(self, "Datablock", has_db_num=True), "Datablock")

        read_layout.addWidget(self.tabs)
        return read_group



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
