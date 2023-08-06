import socket
import socketserver
import time
import threading


def create_socket_conn():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def create_server_conn(addr, host, clientRequestHandler):
    server = socketserver.TCPServer((addr, host), clientRequestHandler)
    server.serve_forever()
    return server


def send_over_socket(addr, data, timeout):
    if(timeout):
        time.sleep(timeout)
    s = create_socket_conn()
    s.connect(addr)
    s.send(data)
    s.close()
    return True


def send_message(addr, data, timeout=None):
    threading.Thread(target=send_over_socket,
                     args=(addr, data, timeout, )).start()
