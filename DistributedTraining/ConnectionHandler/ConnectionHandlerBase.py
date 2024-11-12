import threading
import socket

from typing import *

from abc import ABC, abstractmethod

class ConnectionHandlerBase(ABC):
    def __init__(self, address: Tuple[str, str]):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(address)
        self._running = False
        self._init_resources()
        
    @abstractmethod
    def _init_resources(self):...
        
    @abstractmethod
    def startListening(self): ...
    
    @abstractmethod
    def stopListening(self): ...
    
    @abstractmethod
    def handleConnectionRequest(self, **kwargs): ...
    
    @abstractmethod
    def sendMessage(self, **kwargs): ...
    
    @abstractmethod
    def recvMessage(self, **kwargs): ...
    
    @abstractmethod
    def cleanResources(self, **kwargs): ...
    