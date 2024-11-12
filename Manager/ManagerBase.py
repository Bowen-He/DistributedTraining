from typing import *
from abc import ABC, abstractmethod


class ManagerBase(ABC):
    def __init__(self, manager_address: str, user_port: str, mapper_port: str, reducer_port: str):
        """
        Initialize the manager
        """
        self._manager_address = manager_address
        self._user_port = user_port
        self._mapper_port = mapper_port
        self._reducer_port = reducer_port
        
        self._mapper_conn = []
        self._reducer_conn = None
        
        # Flags indicating the current status of the manager
        self._running = False
        self._busy = False
        
        self._model = None
        self._optimizer = None
        self._conf = None

    @abstractmethod
    def startListeningUser(self):...
    
    @abstractmethod
    def handleUserConnection(self, socket):...
    
    @abstractmethod
    def startListeningMapper(self):...
    
    @abstractmethod
    def handleMapperConnection(self, socket):...
    
    @abstractmethod
    def startListeningReducer(self):...
    
    @abstractmethod
    def handleReducerConnection(self, socket):...
    
    @abstractmethod
    def start(self):...
    
    @abstractmethod
    def stop(self):...
    
