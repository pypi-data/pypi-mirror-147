from socket import socket, SOCK_STREAM, AF_INET
from suef_simpletcp.BaseConnection import BaseConnection

class Client(BaseConnection):
    """
    Client Klasse
    @param ip: IP des Servers, mit dem verbunden werden soll
    @param port: Port des Servers, mit dem verbunden werden soll
    
    Verwendung:
    from TCP import Client
    # Option 1
    client = Client('127.0.0.1', 33996)
    client.start()
    client.send('Ping')
    response = client.get()
    print(response)
    
    # Option 2:
    with Client('127.0.0.1', 33996) as client:
        client.send('Ping')
        response = client.get()
        print(response)
    """
    def __init__(self, ip="0.0.0.0", port=33996):
        super().__init__(socket(AF_INET, SOCK_STREAM), (ip, port))

    def start(self):
        self.conn.connect((self.ip, self.port))
    
    def __enter__(self):
        self.start()
        return self
    
    # def __exit__(self, exc_type, exc_value, traceback):
    def __exit__(self, *args):
        self.conn.close()
