from PyQt6.QtCore import QThread, pyqtSignal

class ConnectionThread(QThread):
    signal = pyqtSignal(bool)

    def __init__(self, plc):
        super().__init__()
        self.plc = plc

    def run(self):
        connection_status = self.plc.connect()
        self.signal.emit(connection_status)