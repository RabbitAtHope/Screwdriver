#===========================#
# I M P O R T S             #
#===========================#

import os
import platform
import socket
import threading

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

client_socket = None

#===========================#

def handle_client(client_socket, client_address):
    try:
    
        print(f"|  [{bcolors.OKGREEN}>{bcolors.ENDC}] Connection from [{bcolors.OKCYAN}{client_address}{bcolors.ENDC}].")
        
        while True:
            data = client_socket.recv(1024)  # Buffer size is 1024 bytes
            if not data:
                break
            print(f"|   [{bcolors.OKGREEN}>{bcolors.ENDC}] Received: [{bcolors.WARNING}{data.decode('utf-8', errors='replace')}{bcolors.ENDC}]")
    
    except ConnectionError:
        print(f"|  [{bcolors.WARNING}x{bcolors.ENDC}] Connection error with [{bcolors.OKCYAN}{client_address}{bcolors.ENDC}].")
    
    finally:
        client_socket.close()
        print(f"|  [{bcolors.WARNING}x{bcolors.ENDC}] Connection with [{bcolors.OKCYAN}{client_address}{bcolors.ENDC}] closed.")

#===========================#

def close_client_connection():

    client_socket.close()
    
    print(f"| [{bcolors.FAIL}x{bcolors.ENDC}] Connection closed.")

#===========================#

def connect_to_server(host='127.0.0.1', port=12345):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    
        try:
    
            # Connect to the server
            client_socket.connect((host, port))
            
            print(f"| [{bcolors.OKGREEN}>{bcolors.ENDC}] Connected to [{bcolors.WARNING}{host}:{port}{bcolors.ENDC}]")

        except Exception as e:
        
            print(f"| [{bcolors.WARNING}x{bcolors.ENDC}] Error: {e}")

#===========================#

def send_data(message="Hello, Server!"):

    # Send the message
    client_socket.sendall(message.encode('utf-8'))
    
    print(f"| [{bcolors.OKGREEN}>{bcolors.ENDC}] Sent: [{bcolors.OKCYAN}{message}{bcolors.ENDC}]")

#===========================#

def start_server(host='0.0.0.0', port=12345):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    
        # Bind the server to the host and port
        server_socket.bind((host, port))
        # Listen for incoming connections
        server_socket.listen()
        
        print(f"| [{bcolors.OKGREEN}>{bcolors.ENDC}] Listening on [{bcolors.WARNING}{host}:{port}{bcolors.ENDC}]...")

        while True:
            try:
            
                client_socket, client_address = server_socket.accept()
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
                client_thread.daemon = True
                client_thread.start()
                
            except KeyboardInterrupt:
                print(f"| [{bcolors.WARNING}x{bcolors.ENDC}] Server shutting down...")
                break
            except Exception as e:
                print(f"| [{bcolors.WARNING}x{bcolors.ENDC}] Error: {e}")

#===========================#

if __name__ == "__main__":

    # Get host information.
    hostname = socket.gethostname()
    hostIP = socket.gethostbyname(hostname)
    systemInfo = platform.system()
    processorInfo = platform.processor()
    alive_host = False

    # Print host information.
    print(f"| [{bcolors.OKGREEN}>{bcolors.ENDC}] [{bcolors.WARNING}" + hostIP + f"{bcolors.ENDC}] [{bcolors.OKGREEN}" + hostname + f"{bcolors.ENDC}] [{bcolors.OKGREEN}" + systemInfo + f"{bcolors.ENDC}] [{bcolors.OKGREEN}" + processorInfo + f"{bcolors.ENDC}]")

    start_server(port=12345)
