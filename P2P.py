import socket

class P2P_server():
    def __init__(self, port=1111, max_connections=1):
        self.object_socket = socket.socket()
        self.port = port
        self.max_connections = max_connections

    def bind_socket(self):
        host_name = socket.gethostname()
        ip_address = socket.gethostbyname(host_name)
        self.object_socket.bind((ip_address, self.port)) # Binds connection to a host and port.

    def listen_socket(self):
        self.object_socket.listen(self.max_connections) # Now accepts connections, limited to the amount given by the argument.

    def new_connection(self):
        print("Waiting for a connection...")
        conn, address = self.object_socket.accept() # This methods returns a NEW socket object for the actual connection.
        print("Connected to:", address)
        return conn, address

    def send_data(self, conn):
        data = input(' -> ')
        conn.sendall(data.encode()) # Send data to the client.

    def run_server(self):
        self.bind_socket()
        self.listen_socket()
        print(self.object_socket.getsockname())
        conn, address = self.new_connection() # Stops here and awaits a connection.
        while True:
            data = conn.recv(1024).decode() # Will await a response from client.
            if not data: break
            print("Client said:", str(data))
            self.send_data(conn)
        print("Closing connection to:", address)
        conn.close() # Close the connection

class P2P_client(P2P_server):
    def connect_to_network(self, target):
        self.object_socket.connect(target)

    def recieve_data(self, socket):
        reply = socket.recv(1024).decode()
        print("Server said:", reply)

    def run_client(self):
        while True:
            self.send_data(self.object_socket)
            self.recieve_data(self.object_socket)
        # self.object_socket.close()

# SERVER = P2P_server(1111)
# SERVER.run_server()
# CLIENT = P2P_client(1112)
# CLIENT.connect_to_network((socket.gethostname(), 1111))
# CLIENT.run_client()