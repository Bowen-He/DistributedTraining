from DistributedTraining.ConnectionHandler import ConnectionHandlerBase
from DistributedTraining.utils import is_socket_alive
import threading

__all__ = ['UserConnectionHandler', 'MapperConnectionHandler', 'ReducerConnectionHandler']

class UserConnectionHandler(ConnectionHandlerBase):
    def __init__(self, address):
        super().__init__(address)
    
    def _init_resources(self):
        self._thread_pool = []
        
    def startListening(self, callback):
        self._server_socket.listen()
        self._running = True
        while self._running:
            client_socket, addr = self._server_socket.accept()
            self.handleConnectionRequest(client_socket=client_socket, callback=callback)
            
    def stopListening(self):
        self._running = False
        
    def handleConnectionRequest(self, **kwargs):
        callback = kwargs['callback']
        client_socket = kwargs['client_socket']
        message = callback(client_socket)
        print(message)

class MapperConnectionHandler(ConnectionHandlerBase):
    def __init__(self, address):
        super().__init__(address)
        
    def _init_resources(self):
        self._client_sockets = {}
        self._client_sockets_lock = threading.Lock()
    
    def startListening(self):
        self._server_socket.listen(10)
        self._running = True
        while self._running:
            client_socket, addr = self._server_socket.accept()
            handle_request_thread = threading.Thread(target=self.handleConnectionRequest, kwargs={'client_socket':client_socket, 'client_addr':addr})
            handle_request_thread.start()
        
    def stopListening(self):
        self._running = False
        
    def handleConnectionRequest(self, **kwargs):
        client_socket = kwargs['client_socket']
        client_addr = kwargs['client_addr']
        with self._client_sockets_lock:
            if client_addr in self._client_sockets.keys():
                if is_socket_alive(self._client_sockets[client_addr]):
                    print("Socket is already connected.")
                else:
                    self._client_sockets[client_addr] = client_socket
            else:
                self._client_sockets[client_addr] = client_socket
                
        

class ReducerConnectionHandler(ConnectionHandlerBase):
    def __init__(self, address):
        super().__init__(address)
        
    def _init_resources(self):
        self._reducer_socket = None
        self._reducer_addr = None
    
    def startListening(self):
        self._server_socket.listen()
        self._running = True
        while self._running:
            client_socket, addr = self._server_socket.accept()
            handle_request_thread = threading.Thread(target=self.handleConnectionRequest, kwargs={'client_socket':client_socket, 'client_addr':addr})
            handle_request_thread.start()
        
    def stopListening(self):
        self._running = False
        
    def handleConnectionRequest(self, **kwargs):
        client_socket = kwargs['client_socket']
        client_addr = kwargs['client_addr']
        if self._reducer_socket is not None:
            if is_socket_alive(self._reducer_socket):
                print("Reducer socket is already connected.")
            else:
                print("Reducer socket is dead, replacing the old socket.")
                self._reducer_socket = client_socket
                self._reducer_addr = client_addr
        else:
            print("Accepting new reducer socket.")
            self._reducer_socket = client_socket
            self._reducer_addr = client_addr
    
    
            
        