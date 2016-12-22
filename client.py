from PyQt5.QtCore import QDataStream, QIODevice
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket

class Client(QDialog):
    def __init__(self):
        super().__init__()
        self.tcpSocket = QTcpSocket(self)
        self.blockSize = 0
        self.makeRequest()
        self.Send()
        self.Recv()
        self.errorDetection()

    def errorDetection(self):
        self.tcpSocket.error.connect(self.displayError)

    def Recv(self):
        self.tcpSocket.readyRead.connect(self.Read)

    def Send(self):
        self.tcpSocket.write(b'hi, i am a new client')

    def makeRequest(self):
        HOST = '127.0.0.1'
        PORT = 8000
        self.tcpSocket.connectToHost(HOST, PORT, QIODevice.ReadWrite)
        self.tcpSocket.waitForConnected(1000)

    def Read(self):
        print("connected to server . . .")
        self.blockSize = 0
        instr = QDataStream(self.tcpSocket)
        instr.setVersion(QDataStream.Qt_5_0)
        if self.blockSize == 0:
            if self.tcpSocket.bytesAvailable() < 2:
                return
            self.blockSize = instr.readUInt16()
        if self.tcpSocket.bytesAvailable() < self.blockSize:
            return
        print(str(instr.readString(), encoding='ascii'))
    def displayError(self, socketError):
        if socketError == QAbstractSocket.RemoteHostClosedError:
            pass
        else:
            print(self, "The following error occurred: %s." % self.tcpSocket.errorString())


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    client = Client()
    sys.exit(client.exec_())
