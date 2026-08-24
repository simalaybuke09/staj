from PyQt6.QtWidgets import QApplication, QMainWindow , QTableWidgetItem
import sys
from window import Ui_MainWindow
from PLC import (PLC, Data, Datablock, Input, Output, Marker, DataType, Params, Read_Bool, Write_Bool, Read_Int, Read_Word, Read_Dword, Read_Byte, Read_Real, Write_Byte, Write_Dword, Write_Int, Write_Real, Write_Word, Write_String, Read_String)
import pandas as pd

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.plc = PLC(ip = "192.168.0.1",rack= 0, slot=1)
        self.plc.connect()

        self.ui.submit.clicked.connect(self.submit_clicked)
        self.ui.ExcelButton.clicked.connect(self.ExcelButton_clicked)
        self.ui.pushButton.clicked.connect(self.push_clicked)
        self.ui.ExcelWriteButton.clicked.connect(self.Write_Excecl_clicked)
         
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

    def push_clicked(self):
        veri = self.ui.veri.currentText()
        data = self.ui.data.currentText()
        size = self.ui.size.currentText()
        start = self.ui.startAddress.text() 
        boolindex = self.ui.boolIndex.text()
        db_number = self.ui.db_number.text()
        deger = self.ui.deger.text()

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
            bool_degeri = deger in ["1", "True", "true", "TRUE"]
            param = Write_Bool(byte_index =0, bool_index=int(boolindex), value = bool_degeri)
        elif data == "Byte":
            param = Write_Byte(byte_index =0 , _int = int(deger))
        elif data == "Int":
            param = Write_Int(byte_index = 0, _int = int(deger))
        elif data == "Word":
            param = Write_Word(byte_index =0 , _int = int(deger))
        elif data == "DWord":
            param = Write_Dword(byte_index =0 , _int = int(deger))
        elif data == "Real":
            param = Write_Real(byte_index =0 , real = float(deger))
        elif data == "String":
            param = Write_String(byte_index =0 , _int = len(deger), value = str(deger), max_size = 254)


        schema = {   
                    "yazilacak_veri" : param
                } 
        try: 

            if type(nesne) == Datablock:
                cikti = nesne.write(db_number=int(db_number), schema=schema)
            else:
                cikti = nesne.write(schema=schema)

            self.ui.result.setText("istenilen veri yazildi")

        except Exception as e:
            self.ui.result.setText(str(e))


    def ExcelButton_clicked(self):
         #excelden gelen veriler için dict
        # Input: { Bool_0 : param1
        #          Int_8 : param2
        #}
        # bu şekilde diğer veri tipleri için de ayrı dict oluştururuz. Çünkü PLC'den blokları karışık şekilde çekemeyiz.
        
        schemas = {
            "Input": {},
            "Output": {},
            "Marker": {},
            "Datablock": {}
        }

        liste= [] #tekrar tekrar excel den çekmek yerine nesneleri ve çıktıları listede tutarızve tabloya yazarız
        tablo = self.ui.Tablo

        
        excel_list = pd.read_excel(r"C:\Users\oyunc\Downloads\staj\07.08.2026\Config.xlsx")

        for index, row in excel_list.iterrows():

            veri_tipi= row["Veri Tipi"]
            data = row["Data Tipi"]
            start = int(row["Başlangıç Adresi"])
            size = int(row["Büyüklük"])
            boolindex = int(row["Bool Index"]) if pd.notna(row["Bool Index"]) else 0
            db_number = int(row["DB Numarası"]) if pd.notna(row["DB Numarası"]) else 0

            if data == "Bool":
                param = Read_Bool(byte_index =start, bool_index=int(boolindex))
            elif data == "Byte":
                param = Read_Byte(byte_index = start)
            elif data == "Int":
                param = Read_Int(byte_index = start)
            elif data == "Word":
                param = Read_Word(byte_index =start)
            elif data == "DWord":
                param = Read_Dword(byte_index = start)
            elif data == "Real":
                param = Read_Real(byte_index =start)
            elif data == "String":
                param = Read_String(byte_index =start)

            #veri_tipi_start şeklinde benzersiz anahtar kelime veririz veri tipi sözlüğündeki 
            if veri_tipi == "Datablock":
                anahtar = f"{veri_tipi}_{db_number}_{start}"
            else:
                anahtar = f"{veri_tipi}_{start}"

            #Bu kontrolü db numarasını paketlemek için yapıyoruz. Bundaki amacımız okuma yaparken sadece en son numarası verilmiş olan datablocku okumaması 
            if veri_tipi == "Datablock":  
                if db_number not in schemas[veri_tipi]:
                    schemas[veri_tipi][db_number] = {}
                schemas[veri_tipi][db_number][anahtar] = param
            else:
                schemas[veri_tipi][anahtar ] = param

            list_row ={
                "anahtar": anahtar,
                "Veri Tipi": veri_tipi,
                "Data Tipi": data,
                "Başlangıç Adresi": start,
                "Büyüklük": size,
                "Bool Index": boolindex,
                "DB Numarası": db_number,
                "Değer": ""
            }
            liste.append(list_row)


        #toplu okuma sonrası değerlerin tutulacağı dict
        toplu_okuma = {}

        rehber = {
            "Input" : Input, 
            "Output" : Output,
            "Marker" : Marker,
            "Datablock" : Datablock
        }

        for key, value in schemas.items():
            if len(value) > 0:

                if key == "Datablock":
                    for db_number, alt_schema in value.items():
                        nesne= Datablock(self.plc)
                        nesne.start_bytes = 0
                        nesne.size = 100
                        cikti = nesne.read(db_number=int(db_number), schema = alt_schema)
                        toplu_okuma.update(cikti)
                else:
                    sinif = rehber[key]
                    nesne = sinif(self.plc)
                    nesne.start_bytes = 0
                    nesne.size = 1024
                    cikti = nesne.read(schema = value)
                    toplu_okuma.update(cikti)
            

        #okunan verilerin tabloya yansıtılması 
        tablo.setRowCount(len(liste))

        for row_no, row in enumerate(liste):
            deger = toplu_okuma.get(row["anahtar"])
            row["Değer"] = deger

            tablo.setItem(row_no,0, QTableWidgetItem(str(row["Veri Tipi"])))
            tablo.setItem(row_no,1, QTableWidgetItem(str(row["Data Tipi"])))
            tablo.setItem(row_no,2, QTableWidgetItem(str(row["Başlangıç Adresi"])))     
            tablo.setItem(row_no,3, QTableWidgetItem(str(row["Büyüklük"])))
            tablo.setItem(row_no,4, QTableWidgetItem(str(row["Bool Index"])))
            tablo.setItem(row_no,5, QTableWidgetItem(str(row["DB Numarası"])))
            tablo.setItem(row_no,6, QTableWidgetItem(str(row["Değer"])))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())