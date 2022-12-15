import Blockchain_BP1 as BB

# server_list = {"85.24.73.168": 1112}

blockchain_net = BB.Blockchain_network(proof_difficulty=5)
blockchain_net.start_server(port=1111)
server_thread = blockchain_net.server_handler()
CLIENT1 = blockchain_net.start_client("85.24.73.168", 1112)

print("Comms for blockchain:", blockchain_net.SERVER.communications)