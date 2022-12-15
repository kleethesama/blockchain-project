import Blockchain_BP1 as BB

# server_list = {"85.24.73.168": 1111}

blockchain_net2 = BB.Blockchain_network(proof_difficulty=5)
blockchain_net2.start_server(port=1112)
server_thread = blockchain_net2.server_handler()

print("Comms for blockchain2:", blockchain_net2.SERVER.communications)