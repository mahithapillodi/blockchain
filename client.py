
import grpc
import blockchain_pb2
import blockchain_pb2_grpc
import sys


# Terminate the client
def terminate():
    print("Terminating client.")
    sys.exit(0)

def connect(ip_addr_port_num):
    global SERVER
    SERVER = ip_addr_port_num

# Initialize the client
def init():
    print("Initializing...")
    
    global SERVERS
    SERVERS = {}
    with open("config.conf", "r") as f:
        for line in f:
            SERVERS[int(line.split(" ")[0])] = f'{line.split(" ")[1]}:{line.split(" ")[2].rstrip()}'

    print("SERVERS accepting connections:")
    for node, ip_port in SERVERS.items():
        print(node, ip_port)

    while True:
        try:
            user_input = input(">")
            parsed_input = parse(user_input)
            msg_type = parsed_input[0]

            if  msg_type == "Connect" and len(parsed_input) >= 2 : 
                connect(parsed_input[1])
                
            elif msg_type == "Quit":
                terminate()
                
            else:
                print("Invalid command! Please try again.")

        except KeyboardInterrupt:
            terminate()
            
if __name__ == "__main__":
    init()