from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGroupBox, QLabel, QLineEdit, QSpinBox, 
                             QPushButton, QTabWidget, QTextEdit, QComboBox, QStackedWidget, QMessageBox)
from PyQt6.QtCore import QSize, Qt
import sys
from dataclasses import dataclass
from PLC import PLC, DataType, Params
from read_thread import ReadThread



class readApp(QWidget):
    def __init__(self,main_window, tab_name, has_db_num=False):
        super().__init__()
        self.main_window = main_window
        self.tab_name=tab_name
        self.has_db_num=has_db_num
        self.initUI()

    def initUI(self):

        layout = QVBoxLayout(self)
        input_layout = QHBoxLayout()

        if self.has_db_num:
            input_layout.addWidget(QLabel("Datablock Numarası:"))
            self.db_num= QSpinBox()
            self.db_num.setRange(0, 9999)
            input_layout.addWidget(self.db_num)

            
            input_layout.addWidget(QLabel("Veri Tipi:"))
            self.data_type = QComboBox()
            self.data_type.addItems([e.name for e in DataType])
            input_layout.addWidget(self.data_type)

            input_layout.addWidget(QLabel("Bool Idx:"))
            self.bool_index = QSpinBox()
            self.bool_index.setRange(0, 7)
            input_layout.addWidget(self.bool_index)

        input_layout.addWidget(QLabel("Başlangıç Byte:"))
        self.start_byte = QSpinBox()
        self.start_byte.setRange(0, 9999)
        input_layout.addWidget(self.start_byte)

        input_layout.addWidget(QLabel("Size:"))
        self.size = QSpinBox()
        self.size.setRange(1, 1024)
        input_layout.addWidget(self.size)


        btn_read = QPushButton("Oku")
        input_layout.addWidget(btn_read)

        layout.addLayout(input_layout)

        self.txt_result = QTextEdit()
        layout.addWidget(self.txt_result)

        self.name = self.tab_name

        btn_read.clicked.connect(self.read_data)


    def read_data(self):
        plc=self.main_window.plc 
        start=self.start_byte.value()
        size = self.size.value()
        
        if self.tab_name == "Datablock":
            db = self.db_num.value()
            veri_tipi = DataType[self.data_type.currentText()]
            bool_index = self.bool_index.value()
        
            #ham_veri = plc.read_datablocks(db,start,okunacak_boyut)
            #parametreler = Params(byte_array=ham_veri, byte_index=0, data_type=veri_tipi, bool_index = bool_index)
            #okunan_veri = plc.read_datablock_with_enum(parametreler)
            #self.txt_result.setText(okunan_veri)

        db = 0
        veri_tipi = None
        bool_index = 0

        self.ReadThread = ReadThread( plc ,self.tab_name ,db, start ,size, veri_tipi, bool_index)
        self.ReadThread.signal.connect(self.txt_result.setText)
        self.ReadThread.start()


                