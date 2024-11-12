from .ManagerBase import ManagerBase
from .ConnectionHandlers import *
from utils.sockets import is_socket_alive

import threading
import time
import torch
import pickle
import socket

class StandardManager(ManagerBase):
    def __init__(self, manager_address: str, user_port: str, mapper_port: str, reducer_port: str):
        super().__init__(manager_address, user_port, mapper_port, reducer_port)
        
    def _init_resources(self):
        self._user_connection_handler = UserConnectionHandler((self._manager_address, self._user_port))
        self._mapper_connection_handler = MapperConnectionHandler((self._manager_address, self._mapper_port))
        self._reducer_connection_handler = ReducerConnectionHandler((self._manager_address, self._reducer_port))
        self._thread_pool = {}
    
    def start(self):
        self._running = True
        self._thread_pool['user_thread'] = threading.Thread(target=self._user_connection_handler.startListening, args=(self.handle_computation,))
        self._thread_pool['mapper_thread'] = threading.Thread(target=self._mapper_connection_handler.startListening)
        self._thread_pool['reducer_thread'] = threading.Thread(target=self._reducer_connection_handler.startListening)
        for key, value in self._thread_pool.items():
            value.start()
    
    def stop(self):
        self._running = False
        
    def handle_computation(self, user_socket):
        if self._busy:
            return "Currently Busy, Try again later."
        else:
            self._busy = True
            return "Initialized training."
            
        
        
            
