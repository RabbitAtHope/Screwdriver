#===========================#
# I M P O R T S             #
#===========================#

import socket

#===========================#
# C O L O R S               #
#===========================#

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    BACKGROUND_MAGENTA = '\033[105m'
    BACKGROUND_WHITE = '\033[47m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    ORANGE = YELLOW

os.system("color") # Comment out on Linux

#===========================#

def send_data(host='127.0.0.1', port=12345, message="Hello, Server!"):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    
        # Connect to the server
        client_socket.connect((host, port))
        
        print(f"| [{bcolors.OKGREEN}>{bcolors.ENDC}] Connected to [{host}:{port}]")

        # Send the message
        client_socket.sendall(message.encode('utf-8'))
        
        print(f"| [{bcolors.OKGREEN}>{bcolors.ENDC}] Sent: [{message}]")

#===========================#

def start_server(host='0.0.0.0', port=12345):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    
        # Bind the server to the host and port
        server_socket.bind((host, port))
        # Listen for incoming connections
        server_socket.listen()
        
        print(f"| [{bcolors.OKGREEN}>{bcolors.ENDC}] Listening on [{host}:{port}]...")

        # Accept a connection
        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                print(f"| [{bcolors.OKGREEN}>{bcolors.ENDC}] Connection from [{client_address}].")
                while True:
                    data = client_socket.recv(1024)  # Buffer size is 1024 bytes
                    if not data:
                        break
                    print(f"| [{bcolors.OKGREEN}>{bcolors.ENDC}] Received: [{data.decode('utf-8')}]")

#===========================#

if __name__ == "__main__":
    start_server(port=12345)
