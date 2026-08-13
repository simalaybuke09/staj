from snap7.client import Client
from snap7.util import get_byte, get_word, get_dword, set_byte, set_word, set_dword, get_bool, set_bool, get_int, set_int, get_real, set_real, get_string, set_string
from enum import Enum
from dataclasses import dataclass
from typing import Any
import snap7.util as util

class DataType(Enum):
    BYTE = "byte"
    WORD = "word"
    DWORD = "dword"
    BOOL = "bool"
    INT = "int"
    REAL = "real"
    STRING = "string"

@dataclass
class Params:
    byte_array: bytearray
    byte_index: int
    data_type: DataType
    

@dataclass
class WordandDwordandInt(Params): #yazma için sadece
    _int: int 

@dataclass
class StringWrite(Params):
    _int: int
    value: str
    max_size: int 


@dataclass
class BoolRead(Params):
    bool_index: int 

@dataclass
class BoolWrite(BoolRead): 
    value: Any  

@dataclass
class RealWrite(Params):
    byte_index: int
    real: bool | str | float | int

class PLC:
    def __init__(self, ip: str, rack: int, slot: int, tcpport: int = 102) -> None:

        self.ip=ip
        self.rack = rack
        self.slot=slot
        self.tcpport= tcpport
        self.client = Client()  

    #bağlantı kontrolü
    def connect(self) -> bool:
        """
        Oluşturulmuş PLC nesnesine bağlanmak için 
        Returns:
            bool: Bağlantı başarılı ise True, değilse False döndürür.

        """
        try:
            self.client.connect(self.ip, self.rack, self.slot, self.tcpport)
            print(f"Bağlantı başarılı")
            return True
        except:
            print(f"Bağlantı başarısız")
            return False

    def disconnect(self):
        """
        Bağlantıyı kapatmak için kullanılır.
        """
        self.client.disconnect()
        print("Bağlantı kapatıldı")


class Data:
    start_bytes: int
    size: int

    def __init__(self, plc:PLC):
        self.plc=plc

    def read(self,start_bytes: int, size: int):
        pass

    def decode_value(self, params: Params):
        method_name = f"get_{params.data_type.name.lower()}"
        method: callable = getattr(util, method_name) 
        if params.data_type == DataType.BOOL:
            return method(params.byte_array, params.byte_index, params.bool_index)
        else:
            return method(params.byte_array, params.byte_index)

    def parse_schema(self, ham_veri: bytearray, schema: dict):
        ayrilmis_veriler = {}

        for degisken, ayarlar in schema.items():
            if ayarlar["type"] == DataType.BOOL:
                param = BoolRead(ham_veri=bytearray,byte_index =ayarlar["byte_index"], data_type=ayarlar["type"], bool_index=ayarlar["bool_index"])
            else:
                param = Params(ham_veri=bytearray,byte_index =ayarlar["byte_index"], data_type=ayarlar["type"])

            ayrilmis_veriler[degisken] = self.decode_value(param)
        return ayrilmis_veriler

class Input(Data):
    def __init__(self, plc:PLC):
        super().__init__(plc)

    def read(self,start_bytes: int, size: int, schema:dict):
        super().read(start_bytes, size)
        ham_veri =self.plc.client.eb_read(start_bytes, size)
        return self.parse_schema(ham_veri, schema)

class Output(Data):
    def read(self,start_bytes: int, size: int,schema:dict):
        super().read(start_bytes, size)
        ham_veri =self.plc.client.ab_read(start_bytes, size)
        return self.parse_schema(ham_veri, schema)


class Marker(Data):
    def read(self,start_bytes: int, size: int, schema:dict):
        super().read(start_bytes, size)
        ham_veri = self.plc.client.mb_read(start_bytes, size)
        return self.parse_schema(ham_veri, schema)
        
class Datablock(Data):
    def read(self,db_number: int,start_bytes:int , size: int , schema:dict):
        super().read(start_bytes, size)
        ham_veri= self.plc.client.db_read(db_number,start_bytes, size)
        return self.parse_schema(ham_veri, schema)
