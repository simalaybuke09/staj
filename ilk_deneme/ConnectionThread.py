from PyQt6.QtCore import QThread, pyqtSignal
from PLC import PLC

class ConnectionThread(QThread):
    signal = pyqtSignal(bool)

    def __init__(self, plc: PLC):
        super().__init__()
        self.plc = plc

    def run(self):
        connection_status = self.plc.connect()
        self.signal.emit(connection_status)