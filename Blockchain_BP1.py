import hashlib, json
from time import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.new_block(previous_hash="The Times 03/Jan/2009 Chancellor on brink of second bailout for banks.", proof=100)

# Create a new block listing key/value pairs of block information in a JSON object. Reset the list of pending transactions & append the newest block to the chain.

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain),
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block

#Search the blockchain for the most recent block.

    @property
    def last_block(self):
        return self.chain[-1]

# Add a transaction with relevant info to the 'blockpool' - list of pending tx's. 

    def new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)
        return self.last_block['index'] + 1

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

blockchain = Blockchain()

t1 = blockchain.new_transaction("Frederik", "Mike", '5 BTC')
t2 = blockchain.new_transaction("Mike", "Satoshi", '1 BTC')
t3 = blockchain.new_transaction("Satoshi", "Hal Finney", '5 BTC')
blockchain.new_block(12345)

t4 = blockchain.new_transaction("Frederik", "Mike", '5 BTC')
t5 = blockchain.new_transaction("Mike", "Satoshi", '1 BTC')
t6 = blockchain.new_transaction("Satoshi", "Hal Finney", '5 BTC')
blockchain.new_block(12345)

# Tests of new task implementations.
blockchain.print_info()

print("Hash comparison:", blockchain.compare_hash(blockchain.get_block(1), blockchain.get_block(2))) # Will (or should) never return True because the timestamp is part of the hash.

print("Chain is valid:", blockchain.validate_chain())