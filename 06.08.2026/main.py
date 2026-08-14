from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
from window import Ui_MainWindow
from PLC import (PLC, Data, Datablock, Input, Output, Marker, DataType, Params, Read_Bool, Write_Bool, Read_Int, Read_Word, Read_Dword, Read_Byte, Read_Real, Write_Byte, Write_Dword, Write_Int, Write_Real, Write_Word, Write_String, Read_String)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.plc = PLC(ip = "192.168.0.1",rack= 0, slot=1)
        self.plc.connect()

        self.ui.submit.clicked.connect(self.submit_clicked)

    def submit_clicked(self):
        veri = self.ui.veri.currentText()
        data = self.ui.data.currentText()
        size = self.ui.size.currentText()
        start = self.ui.startAddress.text()
        boolindex = self.ui.boolIndex.text()
        db_number = self.ui.db_number.text()
        

        if veri == "Input":
            nesne = Input(self.plc)
        elif veri == "Output":
            nesne = Output(self.plc)
        elif veri == "Marker":
            nesne = Marker(self.plc)
        elif veri == "Datablock":
            nesne = Datablock(self.plc)
        nesne.start_bytes = int(start)
        nesne.size = int(size)


        if data == "Bool":
            param = Read_Bool(byte_index =0, bool_index=int(boolindex))
        elif data == "Byte":
            param = Read_Byte(byte_index =0)
        elif data == "Int":
            param = Read_Int(byte_index = 0)
        elif data == "Word":
            param = Read_Word(byte_index =0)
        elif data == "DWord":
            param = Read_Dword(byte_index =0)
        elif data == "Real":
            param = Read_Real(byte_index =0)
        elif data == "String":
            param = Read_String(byte_index =0)


        schema = {   
            "okunan_veri" : param
        }

        if type(nesne) == Datablock:
            cikti = nesne.read(db_number=int(db_number), schema=schema)
        else:
            cikti = nesne.read(schema=schema)
        
        self.ui.result.setText(str(cikti["okunan_veri"]))
        

    
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())