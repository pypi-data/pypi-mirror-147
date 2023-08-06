import socket
from typing import Tuple, Union

class BaseConnection:
    """
    Wrapper für die Funktionen `recv` und `send` von `socket.socket`
    """
    def __init__(self, CConn: socket.socket, CAddr: Tuple[str, int]):
        self.ip = CAddr[0]
        self.port = CAddr[1]
        self.conn = CConn

    def send(self, msg: Union[str, bytes]):
        if type(msg) == type(str()):
            msg = msg.encode()
        elif type(msg) != type(bytes()):
            raise ValueError(f"'msg' muss vom Typ bytes oder string sein. Erhalten: {type(msg)}")
        self.conn.send(msg)

    def get(self, buffer=1024, decode=True):
        message = self.conn.recv(buffer)
        return message.decode() if decode else message
    def __str__(self):
        return f"BaseConnection(ip={self.ip}, port={self.port})"