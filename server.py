import threading


class Server:
    def __init__(self):
        import socket
        self.maxConnections = 4
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 2706
        self.bufferSize = 1024
        self.clientIPs = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        print("SERVER STARTING..")

    def createServer(self):
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handleClient(conn, addr))
            thread.start()
            print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}')

    def handleClient(self, connection, address):
        print(f'[NEW CONNECTION] {address} connected.')
        connected = True
        while connected:
            byteMessage = connection.recv(self.bufferSize)
            msg = byteMessage.decode()[0]
            print(f'{msg}')

    def getIP(self):
        return self.host



server = Server()
print(server.getIP())
server.createServer()
print("lol")
