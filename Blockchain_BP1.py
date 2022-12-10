import hashlib, json, serverClient
from time import time
from threading import Thread

class Blockchain(object):
    def __init__(self, proof_difficulty):
        self.chain = []
        self.header_hashes = []
        self.pending_transactions = []
        self.chain.append(self.new_block(proof=None, previous_hash=None))
        self.header_hashes.append(self.hash(self.chain[0]))
        self.difficulty = "0" * proof_difficulty

    # Create a new block listing key/value pairs of block information in a JSON object. Reset the list of pending transactions & append the newest block to the chain.
    def new_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain),
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }
        return block

    # Verifies the proof for the latest block using the given nonce.
    def verify_proof(self, nonce):
        proof = hashlib.sha256(self.header_hashes[len(self.header_hashes) - 2].encode() + str(nonce).encode()).hexdigest()
        if proof[:len(self.difficulty)] == self.difficulty:
            return True
        else:
            return False
    
    # Adds the given block to the blockchain if its proof is valid.
    def append_block_if_proof(self, block):
        if self.verify_proof(block["proof"]):
            self.chain.append(block)
            return True
        else:
            ValueError("Proof not valid!")
            return False

    # A function that calls two other functions to execute the task of adding/mining a block to the blockchain.
    # Intended to be the main function for adding/mining blocks.
    def mine_block(self):
        new_block = self.new_block(proof=self.proof_of_work(), previous_hash=self.header_hashes[-1])
        self.append_block_if_proof(new_block)
        return True

    # Add a transaction with relevant info to the 'blockpool' - list of pending tx's. 
    def new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)
        return self.chain[-1]['index'] + 1

    # receive one block. Turn it into a string, turn that into Unicode (for hashing). Hash with SHA256 encryption, then translate the Unicode into a hexidecimal string.
    def hash(self, block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()
        raw_hash = hashlib.sha256(block_string)
        return raw_hash.hexdigest()
    
    # Prints all information contained in every block on the blockchain.
    def print_info(self):
        for i in self.chain:
            for u in i:
                print(u + ":", i[u])

    # Returns the block object using its index value.
    def get_block(self, n):
        return self.chain[n]

    # Compares the hashes of two given blocks.
    def compare_hash(self, block1, block2):
        return block1["previous_hash"] == block2["previous_hash"]

    # Validates the entire blockchain by comparing their hashes.
    # This may have to be re-written at some point.
    def validate_chain(self):
        for i in range(len(self.chain) - 1):
            if self.compare_hash(self.chain[i], self.chain[i+1]):
                return False
        return True
    
    # Calculates the required hash for mining a block.
    # Returns the nonce required to verify the proof.
    def proof_of_work(self):
        block_hash = self.header_hashes[-1]
        hash_iteration = ""
        nonce = -1
        while hash_iteration[:len(self.difficulty)] != self.difficulty:
            nonce += 1
            hash_iteration = hashlib.sha256(block_hash.encode() + f"{nonce}".encode()).hexdigest()
        return nonce

class Blockchain_network(Blockchain):
    # Hard-coded dict of all of the members of the network.
    # Has to be changed manually for each new ethernet/wifi network we try it on.
    server_list = {"192.168.43.189": 1112,
                    "192.168.43.189": 1113}

    # Creates a server as an attribute of the class.
    # It'll boot up and wait for clients to connect.
    def start_server(self, port):
        self.SERVER = serverClient.P2P_server(port)
        self.SERVER.run_server()
        self.SERVER.open_for_clients()

    # Creates a client as a socket object and connects to a server. 
    # Returns the socket as the object itself IS the connection, 
    # and makes us able to send data to specific clients at will.
    def start_client(self, address, port):
        CLIENT = serverClient.P2P_client(port)
        CLIENT.connect_to_network((address, port))
        return CLIENT

    # Threader for making the server run in parallel,
    # otherwise it'll block the rest of the program.
    # Having it return the thread object will enable us
    # to control the thread if we need to.
    def server_handler(self, port):
        t = Thread(target=self.start_server, args=(port,))
        t.start()
        return t

    # Sends the entire local server blockchain to a client. 
    # JSON casts the entire blockchain to a string, 
    # so it can be sent through the socket.
    def send_blockchain(self, client):
        data = json.dumps(self.chain)
        client.send_data(client.object_socket, data)
        print("Blockchain sent to:", client.object_socket.getsockname())

    # Parses recieved data and returns it. 
    # In this case it'll be a blockchain string parsed to a blockchain list.
    def recieve_blockchain(self, index):
        data = json.loads(self.SERVER.communications[index])
        return data

# Creates the blockchain and initiates the server for its network.
blockchain_net = Blockchain_network(proof_difficulty=5)
server_thread = blockchain_net.server_handler(port=1111)
blockchain_net.new_transaction("Frederik", "Mike", '5 BTC')
blockchain_net.new_transaction("Mike", "Satoshi", '1 BTC')
blockchain_net.new_transaction("Satoshi", "Hal Finney", '5 BTC')

# Creates a list of connected clients.
clients = []

# Adds client to the list. This will be written as a more convenient function later.
clients.append(blockchain_net.start_client("192.168.43.22", port=1111))
print(clients)

# Sends the local server's blockchain to the client.
# Will also be written as a function that can send to all clients at once.
blockchain_net.send_blockchain(clients[0])

"""
Code used to test for the reciever of the blockchain.

server_thread.join(3.0)
blockchain_net.SERVER.communications[0] = blockchain_net.recieve_blockchain(0)
print(type(blockchain_net.SERVER.communications[0][1]))
print(blockchain_net.hash(blockchain_net.SERVER.communications[0][1])) """

"""
Code used to test for the sender of the blockchain.

blockchain_net.mine_block()

servers = []
servers.append(blockchain_net.start_client("192.168.43.189", 1111))
print(servers)
blockchain_net.send_blockchain(servers[0])

print(blockchain_net.chain[1])
print(type(blockchain_net.chain[1]))
print(blockchain_net.hash(blockchain_net.chain[1])) """

""" 
Code used to test and try a way to have live chat on the blockchain network. Not intended to be implemented any further.

    while True:
    message = input(" -> ")
    for i in clients:
        i.send_data(i.object_socket, message) """