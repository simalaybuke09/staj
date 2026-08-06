from PyQt6.QtCore import QThread, pyqtSignal
from PLC import PLC, DataType, Params
from dataclasses import dataclass


class ReadThread(QThread):
    signal = pyqtSignal(str)
    def __init__(self, plc : PLC ,tab_name : str, db : int, start : int , size : int, veri_tipi : DataType, bool_index : int):
        super().__init__()
        self.plc = plc
        self.tab_name = tab_name
        self.db = db
        self.baslangic_byte = start
        self.size = size
        self.veri_tipi = veri_tipi
        self.bool_index = bool_index



    def run(self):

        
        if self.tab_name == "Datablock":

            
            self.size0 = 0
            if self.veri_tipi in [DataType.BOOL, DataType.BYTE]:
                self.size0 = 1
            elif self.veri_tipi in [DataType.WORD, DataType.REAL]:
                self.size0 = 4
            elif self.veri_tipi in [ DataType.DWORD, DataType.INT]:
                self.size0 = 4
            elif self.veri_tipi == DataType.STRING:
                self.size0 = 254

            ham_veri = self.plc.read_datablocks(self.db ,self.baslangic_byte,self.size0)
            parametreler = Params(byte_array=ham_veri, byte_index=0,size0=self.size0, data_type=self.veri_tipi, bool_index =self.bool_index)
            okunan_veri = self.plc.read_datablock_with_enum(parametreler)
            self.signal.emit(str(okunan_veri))            

        else:
            
            if self.tab_name == "Giriş":
                veri = self.plc.read_inputs(self.baslangic_byte, self.size)
            elif self.tab_name == "Çıkış":
                veri = self.plc.read_outputs(self.baslangic_byte, self.size)
            elif self.tab_name == "Marker":
                veri = self.plc.read_markers(self. baslangic_byte, self.size) 

            self.signal.emit(str(veri))

        
            
