# TCP

This repository contains simplefied classes to use TCP sockets much easier.

## Usage

```python
from multiprocessing import Process
from suef_simpletcp import Server, Client
from suef_simpletcp import BaseConnection

class MyServer(Server):
    def onClientConnect(self, client: BaseConnection):
        while True:
            try:
                if client.get().lower() == 'ping':
                    client.send('Pong!')
            except KeyboardInterrupt:
                pass
    
    def onClientDisconnect(self, client: BaseConnection, error: Exception):
        print(f'Connection to Client (ip: {client.ip}, port: {client.port}) got interrupted. Reason: {error.__class__.__name__}')

if __name__ == "__main__":
    # running server in different process, because it blocks further code execution (it's not asynchronous)
    server = MyServer('127.0.0.1', 1074)
    serverProcess = Process(target=server.start, args=())
    serverProcess.start()


    with Client('127.0.0.1', 1074) as client:
        client.send('ping')
        print(client.get()) # output: Pong!
    serverProcess.terminate()
```
