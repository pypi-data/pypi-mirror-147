from socket import socket, SOCK_STREAM, AF_INET
from suef_simpletcp.BaseConnection import BaseConnection

class Client(BaseConnection):
    """
    @param ip: ip address of the server to connect to
    @param port: port of the server to connect to
    """
    def __init__(self, ip="0.0.0.0", port=33996):
        super().__init__(socket(AF_INET, SOCK_STREAM), (ip, port))

    def start(self) -> None:
        """
        starts the client and connects to the server
        """
        self.conn.connect((self.ip, self.port))
    
    def __enter__(self) -> 'Client':
        self.start()
        return self

    def __exit__(self, *args) -> None:
        self.conn.close()
