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


# Code used to test and try a way to have live chat on the blockchain network. Not intended to be implemented any further.

""" while True:
    message = input(" -> ")
    CLIENT.send_data(CLIENT.object_socket, message) """