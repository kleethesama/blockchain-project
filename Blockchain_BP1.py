import hashlib, json, server_client
from time import time, sleep
from threading import Thread

class Blockchain():
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
    server_list = {"85.24.73.168": 1112}
    
    new_comm = False
    comm_change_index = None

    # Creates a server as an attribute of the class.
    # It'll boot up the server. and wait for clients to connect.
    def start_server(self, port):
        self.SERVER = server_client.P2P_server(port)
        self.SERVER.run_server()
        return self.SERVER.new_clients_handler()

    # Creates a client as a socket object and connects to a server. 
    # Returns the socket as the object itself IS the connection, 
    # and makes us able to send data to specific clients at will.
    def start_client(self, address, port):
        CLIENT = server_client.P2P_client(port)
        CLIENT.connect_to_network((address, port))
        response_thread = CLIENT.client_handler()
        return CLIENT, response_thread

    # Connects to all servers in a server list at once.
    # server_list argument must be a dict.
    def connect_to_servers(self, server_list):
        for i in server_list:
            self.SERVER.clients.append(self.start_client(i, server_list[i]))

    # Sends the entire local server blockchain to a client. 
    # JSON casts the entire blockchain to a string, 
    # so it can be sent through the socket.
    def send_blockchain(self, client):
        data = json.dumps(self.chain)
        print("Sending blockchain to:", client.object_socket.getsockname())
        client.send_data(client.object_socket, data)
        print("Blockchain sent to:", client.object_socket.getsockname())

    # Same as send_blockchain(), but here it's sent to all connected clients.
    def send_blockchain_to_all(self):
        print("Sending blockchain to clients...")
        for i in self.clients:
            self.send_blockchain(i)
        print("Blockchain sent to clients!")

    # Parses recieved data and returns it. 
    # In this case it'll be a blockchain string parsed to a blockchain list.
    def parse_recieved_blockchain(self, index):
        while True:
            if self.SERVER.communications[index]:
                print("Replacing old blockchain with new one...")
                self.chain = json.loads(self.SERVER.communications[index])
                print("Old blockchain replaced!")
                return True
            sleep(1/1000)

    # Threader for the parse_recieved_blockchain() function. 
    # Functions the same way as any of the other threader functions.
    def blockchain_handler(self, index):
        t = Thread(target=self.parse_recieved_blockchain, args=(index,))
        t.start()
        return t

    # Not tested.
    # Checks for any changes in recieved communication from each client.
    def check_comms(self):
        previous_communications = self.SERVER.communications
        while True:
            for i in range(len(self.SERVER.communications)):
                if self.SERVER.communications[i] != previous_communications[i]:
                    self.new_comm = True
                    self.comm_change_index = i
                    print(self.SERVER.communications[i])
                    return True
                else:
                    self.new_comm = False
                    self.comm_change_index = None
            sleep(1/1000)

    # Threader for the check_comms() function.
    # Functions the same way as any of the other threader functions.
    def comms_handler(self):
        t = Thread(target=self.check_comms)
        t.start()
        return t

    def blockchain_network_startup(self, port, server_list):
        print("Local blockchain hash:", self.hash(self.chain))
        server_thread = self.start_server(port)
        self.connect_to_servers(server_list) # Blocks here. Why???
        return server_thread

my_blockchain = Blockchain_network(proof_difficulty=5)
server_thread = my_blockchain.blockchain_network_startup(1111, my_blockchain.server_list)