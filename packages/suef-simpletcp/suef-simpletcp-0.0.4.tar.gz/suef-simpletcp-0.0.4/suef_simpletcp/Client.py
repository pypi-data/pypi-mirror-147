from ctypes import Union
from socket import socket, SOCK_STREAM, AF_INET
from suef_simpletcp.BaseConnection import BaseConnection

class Client(BaseConnection):
    """
    @param ip: ip address of the server to connect to
    @param port: port of the server to connect to
    """
    def __init__(self, ip="0.0.0.0", port=33996):
        super().__init__(socket(AF_INET, SOCK_STREAM), (ip, port))
        self._callbacks = {
            "ServerConnected": [],
            "ServerDisconnected": [],
            "Close": []
        }
    def _callEvent(self, event, *args):
        for callback in self._callbacks[event]:
            callback(*args)
    
    def addListener(self, event: str, callback: callable) -> None:
        """
        Registers a callback for the given event

        Args:
            event (str): The event to register the callback for
            callback (callable): The callback to register
        """
        if event in self._callbacks.keys():
            self._callbacks[event].append(callback)
    def removeListener(self, event: str, callback: callable) -> None:
        """
        Removes a callback from the given event

        Args:
            event (str): The event to remove the callback from
            callback (callable): The callback to remove
        """
        if event in self._callbacks.keys():
            self._callbacks[event].remove(callback)

    def start(self) -> None:
        """
        starts the client and connects to the server
        """
        self.conn.connect((self.ip, self.port))
        self._callEvent("ServerConnected")

    def close(self):
        """
        Closes the connection
        """
        self.conn.close()
        self._callEvent("Close")

    def get(self, buffer: int=1024, decode: bool=False) -> Union[str, bytes]:
        """
        Gets data from the server

        Args:
            buffer (int, optional): The amount of bytes to receive
            decode (bool, optional): Whether to decode the received data to a string

        Returns:
            Union[str, bytes]: The received data
        """
        try:
            return super().get(buffer, decode)
        except (ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError, TimeoutError) as e:
            self._callEvent("ServerDisconnected", self.conn, e)
    
    def send(self, message: Union[str, bytes]) -> None:
        """
        Sends the message to the server

        Args:
            message (str or bytes): The data to send
        """
        try:
            super().send(message)
        except (ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError, TimeoutError) as e:
            self._callEvent("ServerDisconnected", self.conn, e)
    
    def __enter__(self) -> 'Client':
        self.start()
        return self
    
    def __exit__(self, *args) -> None:
        self.close()
