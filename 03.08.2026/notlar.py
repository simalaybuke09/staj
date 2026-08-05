
from snap7 import Client

client = Client()
client.connect("192.168.1.10", 0, 1, tcp_port=1102)
data = client.db_read(1, 0, 4)
client.disconnect()

class snap7.client.Client(lib_location: str | None = None, *, auto_reconnect: bool = False, max_retries: int = 3, retry_delay: float = 1.0, backoff_factor: float = 2.0, max_delay: float = 30.0, heartbeat_interval: float = 0, on_disconnect: Callable[[], None] | None = None, on_reconnect: Callable[[], None] | None = None, **kwargs: Any)

__enter__()→Client
__exit__(exc_type: Any, exc_val: Any, exc_tb: Any)→ None

__init__(lib_location: str | None = None, *, auto_reconnect: bool = False, max_retries: int = 3, retry_delay: float = 1.0, backoff_factor: float = 2.0, max_delay: float = 30.0, heartbeat_interval: float = 0, on_disconnect: Callable[[], None] | None = None, on_reconnect: Callable[[], None] | None = None, **kwargs: Any)
#max_retries – Maksimum yeniden bağlanma denemesi sayısı.
#retry_delay – Yeniden bağlanma girişimleri arasındaki saniye cinsinden ilk gecikme.
#backoff_factor – Yeniden denemeler arasındaki üstel geri çekilme çarpanı.
#max_delay – Yeniden bağlanma girişimleri arasındaki saniye cinsinden maksimum gecikme.
#heartbeat_interval – Kalp atışı probları için saniye cinsinden aralık (0=devre dışı).
#on_disconnect – Bağlantı kesildiğinde isteğe bağlı geri arama başlatılır.
#on_reconnect – Başarılı yeniden bağlanmanın ardından isteğe bağlı geri arama başlatılır.

ab_read(start: int, size: int)→ bytearray
ab_write(start: int, data: bytearray)→ None     

#asenkron 
as_ab_read(start: int, size: int, data: Array | Array | Array | Array | Array | Array)→ int
as_ab_write(start: int, data: bytearray)→ int

#Async PLC belleğini sıkıştırır.
as_compress(timeout: int)→ int
as_decompress(timeout: int)→ int

as_copy_ram_to_rom(timeout: int = 0)→ int

#sayaç alanında asenkron okuma/yazma
as_ct_read(start: int, size: int, data: Array | Array | Array | Array | Array | Array)→ int
as_ct_write(start: int, size: int, data: bytearray)→ int

get_connected()→ bool

async disconnect()→ int

#input
async eb_read(start: int, size: int)→ bytearray

async eb_write(start: int, size: int, data: bytearray)→ int


#output
async ab_read(start: int, size: int)→ bytearray

async ab_write(start: int, data: bytearray)→ int


#blok bilgisi
async get_block_info(block_type: Block, db_number: int)→ TS7BlockInfo


#blok silme 
async delete(block_type: Block, block_num: int)→ int


#marker
async mb_read(start: int, size: int)→ bytearray

async mb_write(start: int, data: bytearray)→ int 

#datablock 
async db_get(db_number: int, size: int = 0)→ bytearray

async db_write(db_number: int, start: int, data: bytearray)→ int

async db_read(db_number: int, start: int, size: int)→ bytearray



(function) def get_byte(
    bytearray_: Buffer,
    byte_index: int
) -> bytes

(function) def set_byte(
    bytearray_: Buffer,
    byte_index: int,
    _int: int
) -> Buffer




(function) def get_word(
    bytearray_: Buffer,
    byte_index: int
) -> bytearray

(function) def set_word(
    bytearray_: Buffer,
    byte_index: int,
    _int: int
) -> Buffer




(function) def get_dword(
    bytearray_: Buffer,
    byte_index: int
) -> int

(function) def set_dword(
    bytearray_: Buffer,
    byte_index: int,
    dword: int
) -> Buffer



(function) def get_bool(
    bytearray_: Buffer,
    byte_index: int,
    bool_index: int
) -> bool

(function) def set_bool(
    bytearray_: Buffer,
    byte_index: int,
    bool_index: int,
    value: bool
) -> Buffer


(function) def get_int(
    bytearray_: Buffer,
    byte_index: int
) -> int

(function) def set_int(
    bytearray_: Buffer,
    byte_index: int,
    _int: int
) -> Buffer

(function) def get_real(
    bytearray_: Buffer,
    byte_index: int
) -> float

(function) def set_real(
    bytearray_: Buffer,
    byte_index: int,
    real: bool | str | float | int
) -> Buffer

(function) def get_string(
    bytearray_: Buffer,
    byte_index: int
) -> str

(function) def set_string(
    bytearray_: Buffer,
    byte_index: int,
    value: str,
    max_size: int = 254
) -> Buffer



#datablock kontrolü
    def read_datablocks(self, db_number:int, size:int) -> bytearray:
        """
        Kullanıcının serbestçe yapılandırdığı, reçeteler, ayarlar, sensör ölçüm değerleri gibi karmaşık verilerin tutulduğu yapılandırılmış hafıza bloklarıdır.

        Args:
            db_number(int): Datablock numarası
            size(int): Datablockten okunacak verinin boyutu


        Returns:
            bytearray
        """
        return self.client.db_read(db_number, size)

    def write_datablocks(self, db_number:int, start:int, data) -> int:
        """
        Args:
            db_number(int): Datablock numarası
            start(int): Bloğun başlangıç byte
            data

        Returns:
            int
        """
        
        return self.client.db_write(db_number, start, data)