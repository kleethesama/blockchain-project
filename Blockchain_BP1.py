import hashlib, json
from time import time

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

    def append_block_if_proof(self, block):
        if self.verify_proof(block["proof"]):
            self.chain.append(block)
            return True
        else:
            ValueError("Proof not valid!")
            return False

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

blockchain = Blockchain(proof_difficulty=5)

t1 = blockchain.new_transaction("Frederik", "Mike", '5 BTC')
t2 = blockchain.new_transaction("Mike", "Satoshi", '1 BTC')
t3 = blockchain.new_transaction("Satoshi", "Hal Finney", '5 BTC')
block1 = blockchain.mine_block()

t4 = blockchain.new_transaction("Frederik", "Mike", '5 BTC')
t5 = blockchain.new_transaction("Mike", "Satoshi", '1 BTC')
t6 = blockchain.new_transaction("Satoshi", "Hal Finney", '5 BTC')
block2 = blockchain.mine_block()