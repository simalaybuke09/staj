
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGroupBox, QLabel, QLineEdit, QSpinBox, 
                             QPushButton, QTabWidget, QTextEdit, QComboBox, QStackedWidget, QMessageBox)
from PLC import PLC
from ConnectionThread import ConnectionThread


class ConnectApp(QWidget):
    def __init__(self,main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
    
        conn_layout = QHBoxLayout(self)

        self.ip_input = QLineEdit()
        conn_layout.addWidget(QLabel("IP:"))
        self.ip_input.setPlaceholderText("Örn: 192.168.1.10")
        conn_layout.addWidget(self.ip_input)

        self.rack_input = QSpinBox()
        conn_layout.addWidget(QLabel("Rack:"))
        conn_layout.addWidget(self.rack_input)

        self.slot_input = QSpinBox()
        conn_layout.addWidget(QLabel("Slot:"))
        conn_layout.addWidget(self.slot_input)

        self.port_input = QSpinBox()
        conn_layout.addWidget(QLabel("Port:"))
        conn_layout.addWidget(self.port_input)
        self.port_input.setRange(1, 65535)

        self.btn_connect = QPushButton("Bağlan")
        conn_layout.addWidget(self.btn_connect)

        self.btn_disconnect = QPushButton("Bağlantıyı Kes")
        conn_layout.addWidget(self.btn_disconnect)

        self.btn_disconnect.setEnabled(False)
        self.status_label = QLabel("Durum: Bağlantı Yok")
        conn_layout.addWidget(self.status_label)


        self.btn_connect.clicked.connect(self.connect_plc)
        self.btn_disconnect.clicked.connect(self.disconnect_plc)


        

    def connect_plc(self): 
        plc=self.main_window.plc
        ip = self.ip_input.text()
        rack = self.rack_input.value()
        slot = self.slot_input.value()
        port = self.port_input.value()
    
        self.main_window.plc = PLC(ip, rack, slot, port)

        self.ConnectionThread = ConnectionThread(self.main_window.plc)
        self.ConnectionThread.signal.connect(self.control_connection_status)
        self.ConnectionThread.start()


    def control_connection_status(self, connection_status):
        self.connection_status = connection_status
        if connection_status:
            self.status_label.setText("Durum: Bağlı")
            self.btn_connect.setEnabled(False)
            self.btn_disconnect.setEnabled(True)
        else:
            self.status_label.setText("Durum: Bağlantı Hatası")
            QMessageBox.critical(self, "Hata", "PLC'ye bağlanılamadı. IP adresini ve ağı kontrol edin.")
            self.plc = None
            self.main_window.plc = None
             


    def disconnect_plc(self):
        plc=self.main_window.plc
        if plc:
            plc.disconnect()
            self.status_label.setText("Durum: Bağlantı Yok")
            self.btn_connect.setEnabled(True)
            self.btn_disconnect.setEnabled(False)
            self.main_window.plc = None
    
