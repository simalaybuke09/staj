from snap7.client import Client
from snap7.util import get_byte, get_word, get_dword, set_byte, set_word, set_dword, get_bool, set_bool, get_int, set_int, get_real, set_real, get_string, set_string
from enum import Enum
from dataclasses import dataclass
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
    # Zorunlu parametreler (Varsayılan değeri olmayanlar üstte olmalı)
    byte_array: bytearray
    byte_index: int
    data_type: DataType
    

    # Opsiyonel parametreler (Varsayılan değerleri olanlar)
    bool_index: int = 0
    max_size: int = 254
    value: Any = None
    _int: int = None
    real: bool | str | float | int = None



    


class PLC:

    """
    Attirbutes:
        ip(str) : PLC'nin IP adresi
        rack(int) : PLC'nin rack numarası (ray numarası)
        slot(int) : PLC'nin slot numarası (yuva numarası)
        tcpport(int) : PLC'nin TCP port numarası (default:102)
        client(Client) : Snap7 kütüphanesiyle iletişim nesnesi 
    """
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

    #input kontrolü
    def read_inputs(self, start_bytes:int , size:int) -> bytearray:
        """
        Args:
            start_bytes(int): Girişten okunacak verinin başlangıç byte
            size(int): Girişten okunacak verinin boyutu

        Returns:
            bytearray

        """
        return self.client.eb_read(start_bytes, size)

    def write_inputs(self, start_bytes:int, size:int, data:bytearray) -> int:
            """
            Args:
                start_bytes(int): Çıktılara yazılacak verinin başlangıç byte
                size(int): Çıktılara yazılacak verinin boyutu
                data(bytearray): Yazılacak veri

            Returns:
                int
        """
            return self.client.eb_write(start_bytes, size, data)

    
    #output kontrolü 
    def read_outputs(self, start_bytes:int, size:int) -> bytearray: 
        """
        Args:
            start_bytes(int): Çıktılardan okunacak verinin başlangıç byte
            size(int): Çıktılardan okunacak verinin boyutu

        Returns:
            bytearray       
        """
        return self.client.ab_read(start_bytes, size)

    def write_outputs(self, start_bytes:int,  data:bytearray) -> int:
        """
        Args:
            start_bytes(int): Girişten okunacak verinin başlangıç byte
            data(bytearray): Yazılacak veri

        Returns:
            int
        """
        return self.client.ab_write(start_bytes,  data)


    #marker kontrolü 
    def read_markers(self, start_bytes:int, size:int) -> bytearray:
        """
        PLC'nin kendi içindeki geçici hesaplamaları veya durumları tuttuğu sanal hafıza alanıdır.

        Args:
            start_bytes(int): Merkerten okunacak verinin başlangıç byte
            size(int): Merkerten okunacak verinin boyutu

        Returns:
            bytearray
        """
        return self.client.mb_read(start_bytes, size)

    #datablock kontrolü
    
    def write_markers(self, start_bytes:int, data:bytearray) -> int:
        """
        Args:
            start_bytes(int): Merkerlara yazılacak verinin başlangıç byte
            data(bytearray): Yazılacak veri

        Returns:
            int
        """
        return self.client.mb_write(start_bytes, data)

    def read_datablocks(self,start_bytes: int, db_number:int, size:int) -> bytearray:
    
        return self.client.db_read(db_number, start_bytes, size)
    
    def write_datablocks(self, db_number:int, start:int, data) -> int:
                
        return self.client.db_write(db_number, start, data)
     

    def read_byte(self, bytearray:bytearray, byte_index:int) -> bytearray:
        return get_byte(bytearray, byte_index)

    def write_byte(self, bytearray:bytearray, byte_index:int, _int:int) -> bytearray:
        return set_byte(bytearray, byte_index, _int)

    def read_word(self, bytearray:bytearray, byte_index:int) -> bytearray:
        return get_word(bytearray, byte_index)

    def write_word(self, bytearray:bytearray, byte_index:int, _int:int) -> bytearray:
        return set_word(bytearray, byte_index, _int)

    def read_dword(self, bytearray:bytearray, byte_index:int) -> int:
        return get_dword(bytearray, byte_index)

    def write_dword(self, bytearray:bytearray, byte_index:int, _int:int) -> bytearray:
        return set_dword(bytearray, byte_index, _int)

    def read_bool(self, bytearray:bytearray, byte_index:int, bool_index:int) -> bool:
        return get_bool(bytearray, byte_index, bool_index)

    def write_bool(self, bytearray:bytearray, byte_index:int, bool_index:int, value:bool) -> bytearray:
        return set_bool(bytearray, byte_index, bool_index, value)

    def read_int(self, bytearray:bytearray, byte_index:int) -> int:
        return get_int(bytearray, byte_index)

    def write_int(self, bytearray:bytearray, byte_index:int, _int:int) -> bytearray:
        return set_int(bytearray, byte_index, _int)

    def read_real(self, bytearray:bytearray, byte_index:int) -> float:
        return get_real(bytearray, byte_index)
    
    def write_real(self, bytearray:bytearray, byte_index:int, real:bool | str | float | int) -> bytearray:
        return set_real(bytearray, byte_index, real)

    def read_string(self, bytearray:bytearray, byte_index:int) -> str:
        return get_string(bytearray, byte_index)

    def write_string(self, bytearray:bytearray, byte_index:int, value:str, max_size:int = 254)  -> bytearray:
        return set_string(bytearray, byte_index, value, max_size)


    
    def read_datablock_with_enum(self, params:Params) :

        method_name = f"read_{params.data_type.name.lower()}"
        method = getattr(self, method_name)

        if params.data_type == DataType.BOOL:
            return method(params.byte_array, params.byte_index, params.bool_index)

        else:
            return method(params.byte_array, params.byte_index)


    def write_datablock_with_enum(self, params:Params) :
    
        method_name = f"read_{DataType}"
        method = getattr(self, method_name)
    
        if params.data_type == DataType.BOOL :
            return method(params.byte_array, params.byte_index, params.bool_index, params.value)

        if params.data_type == DataType.REAL:
            return method(params.byte_array, params.byte_index, params.real)


        if params.data_type == DataType.STRING:
            return method(params.byte_array, params.byte_index, params.max_size)

        else:
            return method(params.byte_array, params.byte_index, params._int)


        

        
        

    


    




# if __name__ == "__main__":
#     plc = PLC(ip="192.168.1.10",rack= 0, slot= 1)
#     plc.connect()

#     if plc.client.get_connected():
        

#         plc.disconnect()