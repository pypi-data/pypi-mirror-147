from ctypes import WinError
from socket import socket, SOCK_STREAM, AF_INET, SO_REUSEADDR, SOL_SOCKET
from multiprocessing import Process
from suef_simpletcp.BaseConnection import BaseConnection

class Server:
    """
    @param ip: ip address the server should bind on
    @param port: port the server should bind on
    """
    def __init__(self, ip: str = "0.0.0.0", port: int = 33996):
        self.ip         = ip
        self.port       = port
        self.s          = socket(AF_INET, SOCK_STREAM)
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    def onClientConnect(self, client: BaseConnection):
        """
        Gets called when a new client connects
        """
        raise NotImplementedError("method `onClientConnect` not implemented")
    def onClientDisconnect(self, client: BaseConnection, error: Exception):
        """
        Gets called when a client disconnects
        """
        pass

    def start(self):
        """
        starts the server and waits for users to connect
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
        waits for incoming user connections and returns a `BaseConnection` object for the new user
        """
        return BaseConnection(*self.s.accept())


    def cH(self, client: BaseConnection):
        """
        calls the `onClientConnect` and `onClientDisconnect` methods
        """
        try:
            try:
                self.onClientConnect(client)
            except (ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError) as e:
                self.onClientDisconnect(client, e)
        except OSError as e:
            pass
