from snap7.client import Client
from snap7.util import get_byte, get_word, get_dword, set_byte, set_word, set_dword, get_bool, set_bool, get_int, set_int, get_real, set_real, get_string, set_string
from enum import Enum
from dataclasses import dataclass, field
from typing import Any


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
    #byte_array: bytearray
    byte_index: int
    #data_type: DataType = field(init=False)
    
    def get(self):
        pass

    def set(self):
        pass

@dataclass
class Write_Word(Params): #yazma için sadece
    _int: int 
    data_type= DataType.WORD
    def set(self,byte_array):
        return set_word(byte_array, self.byte_index,self._int)

@dataclass
class Write_Dword(Params): #yazma için sadece
    _int: int 
    data_type= DataType.DWORD
    def set(self,byte_array):
        return set_dword(byte_array, self.byte_index,self._int)

@dataclass
class Write_Int(Params): #yazma için sadece
    _int: int 
    data_type = DataType.INT
    def set(self,byte_array):
        return set_int(byte_array, self.byte_index,self._int)


@dataclass  
class Write_String(Params):
    _int: int
    value: str
    max_size: int 
    data_type = DataType.STRING
    def set(self,byte_array):
        return set_string(byte_array, self.byte_index, self._int, self._int, self.max_size)

@dataclass
class Read_Bool(Params):
    bool_index: int 
    data_type = DataType.BOOL
    def get(self,byte_array):
        return get_bool(byte_array, self.byte_index, self.bool_index)


@dataclass
class Write_Bool(Read_Bool): 
    value: Any
    bool_index: int  
    data_type = DataType.BOOL
    def set(self, byte_array):
        return set_bool(byte_array, self.byte_index, self.bool_index, self.value)


@dataclass
class Write_Real(Params):
    real: bool | str | float | int
    data_type = DataType.REAL
    def set(self, byte_array):
        return set_real(byte_array, self.byte_index, self.real)

@dataclass
class Read_String(Params):
    data_type = DataType.STRING
    max_size: int = 254

    def get(self, byte_array):
        return get_string(byte_array, self.byte_index)

@dataclass
class Read_Int(Params):
    data_type = DataType.INT
    def get(self, byte_array):
        return get_int(byte_array, self.byte_index)

@dataclass
class Read_Word(Params):
    data_type = DataType.WORD
    def get(self, byte_array):
        return get_word(byte_array, self.byte_index)

@dataclass
class Read_Dword(Params):
    data_type= DataType.DWORD
    def get(self, byte_array):
        return get_dword(byte_array, self.byte_index)

@dataclass
class Read_Byte(Params):
    data_type= DataType.BYTE
    def get(self, byte_array):
        return get_byte(byte_array, self.byte_index)   

@dataclass
class Read_Real(Params):
    data_type = DataType.REAL
    def get(self, byte_array):
        return get_real(byte_array, self.byte_index)

@dataclass
class Write_Byte(Params):
    _int: int
    data_type= DataType.BYTE
    
    def set(self, byte_array):
        return set_byte(byte_array, self.byte_index, self._int)


  

class PLC:
    def __init__(self, ip: str, rack: int, slot: int) -> None:

        self.ip=ip
        self.rack = rack
        self.slot=slot
        self.client = Client()  

    #bağlantı kontrolü
    def connect(self) -> bool:
        """
        Oluşturulmuş PLC nesnesine bağlanmak için 
        Returns:
            bool: Bağlantı başarılı ise True, değilse False döndürür.

        """
        try:
            self.client.connect(self.ip, self.rack, self.slot)
            print(f"Bağlantı başarılı")
            return True
        except Exception as e:
            print(f"Bağlantı başarısız {e}")
            return False

    def disconnect(self):
        """
        Bağlantıyı kapatmak için kullanılır.
        """
        self.client.disconnect()
        print("Bağlantı kapatıldı")


class Data:
    start_bytes: int = 0
    size: int =0 
    

    def __init__(self, plc:PLC):
        self.plc=plc

    def read(self,start_bytes: int, size: int):
        pass

    def _schema(self,ham_veri:bytearray ,schema: dict):
        veriler = {}
        
        for key,value in schema.items():
            veriler[key] = value.get(ham_veri)

        return veriler

    def write(self, start_bytes : int, size : int):
        pass

    def w_schema(self,buffer : bytearray ,schema: dict):
        veriler = {}
        
        for key,value in schema.items():
            value.set(buffer)

        return buffer 

class Input(Data):
    def __init__(self, plc:PLC):
        super().__init__(plc)

    def read(self, schema:dict):
        ham_veri =self.plc.client.eb_read(self.start_bytes, self.size)
        return self._schema(ham_veri, schema)
    def write(self, schema:dict):
        buffer = self.plc.client.eb_read(self.start_bytes, self.size)
        self.w_schema(buffer , schema)
        self.plc.client.eb_write(self.start_bytes, self.size, buffer)
        print("Yazma işlemi başarılı")

class Output(Data):
    def read(self,schema:dict):
        ham_veri =self.plc.client.ab_read(self.start_bytes, self.size)
        return self._schema(ham_veri, schema)
    def write(self,schema:dict ):
        buffer = self.plc.client.ab_read(self.start_bytes, self.size)
        self.w_schema(buffer , schema)
        self.plc.client.ab_write(self.start_bytes,buffer)
        print("Yazma işlemi başarılı")

    
class Marker(Data):
    def read(self,schema:dict):
        ham_veri = self.plc.client.mb_read(self.start_bytes, self.size)
        return self._schema(ham_veri, schema)
    def write(self ,schema:dict ):
        buffer = self.plc.client.mb_read(self.start_bytes, self.size)
        self.w_schema(buffer , schema)
        self.plc.client.mb_write(self.start_bytes, buffer)
        print("Yazma işlemi başarılı")


        
class Datablock(Data):
    def read(self,db_number: int, schema:dict):
        ham_veri= self.plc.client.db_read(db_number,self.start_bytes, self.size)
        return self._schema(ham_veri, schema)
    def write(self, db_number : int, schema:dict):
        buffer = self.plc.client.db_read(db_number,self.start_bytes, self.size)
        self.w_schema(buffer , schema)
        self.plc.client.db_write(db_number, self.start_bytes, buffer)
        print("Yazma işlemi başarılı")
