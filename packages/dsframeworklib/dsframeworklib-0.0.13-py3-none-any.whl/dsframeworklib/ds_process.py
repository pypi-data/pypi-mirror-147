import socketserver


class dServerRequestHandler(socketserver.BaseRequestHandler):
    '''
    Nothing but socketserver.BaseRequestHandler; 

    Need to define handler class method, i.e.\n
    def handle(self):
        pass
    '''

    def __init__(self, request, addr, server):
        socketserver.BaseRequestHandler.__init__(
            self, request, addr, server)

class dServer(socketserver.TCPServer):
    def __init__(self, server_address, handler_class=dServerRequestHandler):
        super().__init__(server_address, handler_class)


if __name__ == "__main__":
    pass
