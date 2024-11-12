import socket

def is_socket_alive(test_socket, message, timeout=1.0):
    try:
        test_socket.setblocking(0)
        test_socket.send(message.encode())
        test_socket.settimeout(timeout)

        data = test_socket.recev(1024)
        return True if data else False
    
    except socket.error as e:
        print('Socket error:', e)
        return False
        
    
    