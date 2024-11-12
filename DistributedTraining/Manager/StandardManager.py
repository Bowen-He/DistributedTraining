from .ManagerBase import ManagerBase
from utils.sockets import is_socket_alive

import threading
import time
import torch
import pickle
import socket

class StandardManager(ManagerBase):
    def __init__(self, manager_address):
        super().__init__(manager_address)
        
    def startListeningUser(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self._manager_address, self._user_port))
        server_socket.listen()
        
        client_socket, addr = server_socket.accept()
        self.handleUserConnection(client_socket)
        
    def handleUserConnection(self, socket):...
    
    def startListeningMapper(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self._manager_address, self._mapper_port))
        server_socket.listen(5)
        
        try:
            while self._running:
                client_socket, addr = server_socket.accept
                client_thread = threading.Thread(target=self.handleMapperConnection, args=(client_socket))
                client_thread.start()
        finally:
            server_socket.close()
            
    def handleMapperConnection(self, socket): ...
    
    def startListeningReducer(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self._manager_address, self._reducer_port))
        server_socket.listen()
        
        try:
            while self._running:
                client_socket, addr = server_socket.accept()
                client_thread = threading.Thread(target=self.handleReducerConnection, args=(client_socket))
                client_thread.start()
        finally:
            server_socket.close()
    
    def handleReducerConnection(self, socket):
        if self._reducer_conn is not None:
           if is_socket_alive(self._reducer_conn):
               print("Reducer is already Connected.")
           else:
               print("Replace dead reducer.")
               self._reducer_conn = socket
        else:
            print("Accept reducer.")
            self._reducer_conn = socket
    
    def start(self):
        pass
    
    def stop(self):
        pass
        
            
