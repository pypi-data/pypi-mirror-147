import socket
from typing import Tuple, Union

class BaseConnection:
    """
    Wrapper of methods `recv` and `send` of the `socket.socket` class
    """
    def __init__(self, CConn: socket.socket, CAddr: Tuple[str, int]):
        self.ip = CAddr[0]
        self.port = CAddr[1]
        self.conn = CConn

    def send(self, msg: Union[str, bytes]) -> None:
        if type(msg) == type(str()):
            msg = msg.encode()
        elif type(msg) != type(bytes()):
            raise ValueError(f"'msg' has to be of type 'str' or 'bytes', got '{type(msg)}' instead.")
        self.conn.send(msg)

    def get(self, buffer=1024, decode=True) -> Union[str, bytes]:
        message = self.conn.recv(buffer)
        return message.decode() if decode else message

    def __str__(self) -> str:
        return f"BaseConnection(ip={self.ip}, port={self.port})"