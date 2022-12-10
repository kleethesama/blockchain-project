import socket, time
from threading import Thread

class P2P_server():
    def __init__(self, port=1111):
        self.object_socket = socket.socket()
        self.port = port
        self.communications = [None]

    def bind_socket(self):
        host_name = socket.gethostname()
        ip_address = socket.gethostbyname(host_name)
        self.object_socket.bind((ip_address, self.port)) # Binds connection to a host and port.

    def listen_socket(self):
        self.object_socket.listen() # Now accepts connections, limited to the amount given by the argument.

    def new_connection(self):
        print("Waiting for a connection...")
        conn, address = self.object_socket.accept() # This methods returns a NEW socket object for the actual connection.
        print("Connected to:", address)
        return conn, address

    def send_data(self, conn, data):
        conn.sendall(data.encode())

    def run_server(self):
        self.bind_socket()
        self.listen_socket()
        print(self.object_socket.getsockname())

    def open_for_clients(self):
        counter = 0
        while True:
            conn, address = self.new_connection() # Stops here and awaits a connection.
            self.communications.append(None)
            t = Thread(target=self.handler, args=(conn, address, counter))
            t.start()
            counter += 1

    def handler(self, client, address, index):
        while True:
            self.communications[index] = client.recv(1024).decode()
            if not self.communications[index]: break
            else:
                print("From " + repr(address) + " -> " + str(self.communications[index]))
                client.sendall("This is a test reply!".encode())
        client.close()
        print("Closed connection to", repr(address))

class P2P_client(P2P_server):
    def client_handler(self):
        t = Thread(target=self.recieve_data)
        t.start()

    def connect_to_network(self, target):
        self.object_socket.connect(target)

    def recieve_data(self):
        while True:
            reply = self.object_socket.recv(1024).decode()
            print("Server said:", reply)

    def run_client(self):
        self.client_handler()

if __name__ == "__main__":
    # SERVER = P2P_server(1111)
    # SERVER.run_server()
    # SERVER.open_for_clients()
    CLIENT = P2P_client()
    CLIENT.connect_to_network((socket.gethostname(), 1111))
    CLIENT.run_client()
    while True:
        CLIENT.send_data(CLIENT.object_socket, input(" -> "))