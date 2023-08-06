from ctypes import WinError
from socket import socket, SOCK_STREAM, AF_INET, SO_REUSEADDR, SOL_SOCKET
from multiprocessing import Process
from suef_simpletcp.BaseConnection import BaseConnection

class Server:
    """
    Server Klasse
    @param ip: IP des Servers
    @param port: Port des Servers
    Verwendung:
    from TCP import Server
    
    class MyServer(Server):
        def onClientConnect(self, client: BaseConnection):
            request = client.get()
            if request.lower() == 'ping:
                client.send('Pong!')
    server = MyServer('127.0.0.1', 33996)
    server.start()
    """
    def __init__(self, ip: str = "0.0.0.0", port: int = 33996):
        self.ip         = ip
        self.port       = port
        self.s          = socket(AF_INET, SOCK_STREAM)
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    def onClientConnect(self, client: BaseConnection):
        """
        Wird aufgerufen, wenn ein Client sich verbunden hat
        """
        raise NotImplementedError("Methode `onClientConnect` nicht implementiert")
    def onClientDisconnect(self, client: BaseConnection, error: Exception):
        """
        Wird aufgerufen wenn die Verbindung zum Client abgebrochen wird
        """
        raise NotImplementedError("Methode `onClientDisconnect` nicht implementiert")

    def start(self):
        """
        Startet den Server
        """
        self.s.bind((self.ip, self.port))
        self.s.listen(5)
        try:
            while True:
                client = self.getNewClient()
                p = Process(target=self.cH, args=(client,))
                p.start()
        except KeyboardInterrupt:
            self.s.close()

    def getNewClient(self):
        """
        Wartet auf eingehende Verbindungen und gibt die Verbindung als `BaseConnection`-Objekt zurück
        """
        return BaseConnection(*self.s.accept())


    def cH(self, client: BaseConnection):
        """
        Client Handler.
        Ruft die Funktion `clientHandler` auf, sofern diese definiert wurde.
        """
        try:
            try:
                self.onClientConnect(client)
            except (ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError) as e:
                self.onClientDisconnect(client, e)
        except WinError as e:
            print('\nERROR')
