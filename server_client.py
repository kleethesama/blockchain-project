import socket
from threading import Thread

class P2P_server():
    # The server will have its own socket object, assigned port, clients it awaits, and a record of recieved data.
    def __init__(self, port=1111):
        self.object_socket = socket.socket()
        self.port = port
        self.clients = []
        self.communications = [None]

    # The socket objects requires assigned self-identification (IP-address) and port.
    def bind_socket(self):
        self.object_socket.bind((socket.gethostname(), self.port)) # Binds connection to a host and port.

    def listen_socket(self):
        self.object_socket.listen() # Now accepts connections, limited to the amount by the argument.

    # The server will wait for an incoming client. This method will not terminate until a connection has been established.
    def new_connection(self):
        print("Waiting for a new client...")
        conn, address = self.object_socket.accept() # This methods returns a NEW socket object for the actual connection.
        print("Accepted client connection from:", address)
        return conn, address

    # Composed method. Executes the necessary methods for having our simple, functional socket.
    def run_server(self):
        self.bind_socket()
        self.listen_socket()
        print(self.object_socket.getsockname()) # The very first thing to be printed. Will show the server's own identity.

    # Method designed to be executed as a thread. It is here that the server continuously checks for new incoming clients.
    # It shouldn't be called on its own, it will block the rest of the code.
    def open_for_clients(self):
        counter = 0 # Used for assigning index numbers to each thread to keep track of who is sending messages.
        threads = [] # Debug
        while True: # Will run indefinitely, but in this case it is as a thread, so it does not block code.
            conn, address = self.new_connection() # Blocks here and awaits a connection. Will continue once a connection has been established.
            t = Thread(target=self.handler, args=(conn, address, counter)) # Creates a new thread to continuously listen for any new incoming data.
            t.start() # Thread will start executing.
            threads.append(t) # Debug
            # Appends a new value to communications. This is to ensure a new communications element can be changed.
            # EXPLAIN FURTHER...
            self.communications.append(None)
            counter += 1 # Counter iterator.
            print("Client counter:", counter) # Debug
            print(f"Comm threads for {self.object_socket.getsockname()}:", threads) # Debug

    # Method designed to be executed as a thread. Handles incoming data and sends "OK" replies each time it recieves anything.
    def handler(self, client, address, index):
        while True: # Will run indefinitely, but in this case it is as a thread, so it does not block code.
            self.communications[index] = client.recv(1024).decode() # Recieved data will assigned to the particular communications element that it was assigned to in open_for_clients().
            if not self.communications[index]: break # If there is no data to be recieved...?
            else:
                print("From", repr(address), "->", self.communications[index]) # Prints the recieved data.
                client.sendall("OK".encode()) # Sends an "OK" reply to the client.
        client.close()
        print("Closed connection to", repr(address))

    # Threader for making the server run in parallel, otherwise it'll block the rest of the program.
    # Having it return the thread object will enable us to control the thread if we need to.
    def new_clients_handler(self):
        t = Thread(target=self.open_for_clients)
        t.start()
        return t

class P2P_client(P2P_server):
    connected = False

    def send_data(self, data):
        print("SENDING:", data, "\n->", self.object_socket.getsockname())
        self.object_socket.sendall(data.encode())
        print("Data sent. Awaiting response...")

    def recieve_data(self):
        while True:
            reply = self.object_socket.recv(1024).decode()
            print(f"Response from {self.object_socket.getsockname()} ->", reply)

    # Threader for the recieve_data() method. It calls the method as a thread and starts it.
    def client_handler(self):
        t = Thread(target=self.recieve_data)
        t.start()
        return t

    def connect_to_network(self, target):
        print("Attempting to connect to:", target)
        while not self.connected:
            try:
                self.object_socket.connect(target)
                self.connected = True
            except ConnectionRefusedError:
                print("Still attempting...")
        print("Connected to:", target)

"""
These blocks of code are for testing. What is expected to happen when you run this script:
Server boots up and waits for clients to connect. It will continuously check for new incoming clients even after its first connection.

Client will attempt to connect to the server. If it fails, it will print a timeout error-message to the terminal.
The client will attempt to send data (encoded string) to the server. If it succeeds, an OK reply will be recieved from the server.

Running both test functions in the same terminal may print information out of order as we are using threading.
Running the functions seperately in each of their own terminals will give better results.

The class attribute "communications" is the server's record of recieved data from clients.
The list's index itself is used to keep track of which client sent the data.
"""
if __name__ == "__main__":
    def test_server():
        SERVER = P2P_server(port=1111) # Instantiate server as an object.
        SERVER.run_server()
        # Assigning the thread to a variable enables us to control it through its methods.
        # It will run regardless of whether or not it is assigned to a variable.
        server_thread = SERVER.new_clients_handler()
        return SERVER

    def test_client(target):
        CLIENT = P2P_client(port=1112) # Instantiate client as an object.
        CLIENT.connect_to_network(target) # Attempt to connect to server.
        response_thread = CLIENT.client_handler() # Start checking for any replies the server may send.
        return CLIENT
    
    # SERVER = test_server()
    CLIENT = test_client((socket.gethostname(), 1111))
    CLIENT.send_data("You can write anything here, but this must be a string.") # Send test-string to server.