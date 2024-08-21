#===========================#
# I M P O R T S             #
#===========================#

import os
import json
import sqlite3
import base64
import shutil
import ctypes
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from win32crypt import CryptUnprotectData
from ctypes.wintypes import MAX_PATH

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

def find_local_state():
    user_profile = os.environ.get("USERPROFILE")
    
    if not user_profile:
        print(f"| [{bcolors.FAIL}x{bcolors.ENDC}] Error getting user path.")
        return ""
    
    local_state_path = os.path.join(user_profile, r"AppData\Local\Google\Chrome\User Data\Local State")
    print(f"| [{bcolors.OKGREEN}>{bcolors.ENDC}] Full path to Local State file: [{bcolors.WARNING}"+str(local_state_path)+f"{bcolors.ENDC}]")
    return local_state_path

def find_login_data():
    user_profile = os.environ.get("USERPROFILE")
    if not user_profile:
        print("| [{bcolors.FAIL}x{bcolors.ENDC}] Error getting user path.")
        return ""
    
    login_data_path = os.path.join(user_profile, r"AppData\Local\Google\Chrome\User Data\Default\Login Data")
    print(f"| [{bcolors.OKGREEN}>{bcolors.ENDC}] Full path to Login Data file: [{bcolors.WARNING}"+str(login_data_path)+f"{bcolors.ENDC}]")
    return login_data_path

def get_encrypted_key(local_state_path):
    try:
        with open(local_state_path, 'r', encoding='utf-8') as file:
            local_state = json.load(file)
        encrypted_key = local_state["os_crypt"]["encrypted_key"]
        
        print(f"| [{bcolors.OKGREEN}>{bcolors.ENDC}] Retrieved encrypted key: [{bcolors.WARNING}"+str(encrypted_key)[:50]+f"...{bcolors.ENDC}]")
        
        return encrypted_key
        
    except (FileNotFoundError, KeyError) as e:
        print(f"| [{bcolors.FAIL}x{bcolors.ENDC}] Error: {e}")
        return ""

def decrypt_key(encrypted_key):

    encrypted_key = base64.b64decode(encrypted_key)[5:]  # Remove "DPAPI" prefix
    decrypted_key = CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    
    print(f"| [{bcolors.OKGREEN}>{bcolors.ENDC}] Decrypted key: [{bcolors.WARNING}"+str(decrypted_key)[:50]+f"...{bcolors.ENDC}]")
    
    return decrypted_key

def login_data_parser(login_data_path, decryption_key):

    print(f"| [{bcolors.OKGREEN}>{bcolors.ENDC}] Parsing password data.")

    try:
    
        temp_login_data_path = login_data_path + 'a'
        shutil.copyfile(login_data_path, temp_login_data_path)
        
        conn = sqlite3.connect(temp_login_data_path)
        
        print(f"| [{bcolors.OKGREEN}>{bcolors.ENDC}] Connected to SQL database.")
        
        cursor = conn.cursor()
        
        print(f"| [{bcolors.OKGREEN}>{bcolors.ENDC}] Created cursor.")
        
        cursor.execute("SELECT origin_url, username_value, password_value, blacklisted_by_user FROM logins")
        
        print(f"| [{bcolors.OKGREEN}>{bcolors.ENDC}] Executed username and password retrieval query.")

        for row in cursor.fetchall():
        
            origin_url, username_value, encrypted_password, blacklisted_by_user = row
            
            if origin_url and username_value and not blacklisted_by_user:
            
                iv = encrypted_password[3:15]
                encrypted_password = encrypted_password[15:]
                
                cipher = AES.new(decryption_key, AES.MODE_GCM, iv)
                decrypted_password = cipher.decrypt(encrypted_password).decode('utf-8')
                
                print(f" [{bcolors.OKGREEN}>{bcolors.ENDC}] 🔗 URL: [{bcolors.OKCYAN}" + origin_url + f"{bcolors.ENDC}]")
                print(f" [{bcolors.OKGREEN}>{bcolors.ENDC}] 👤 Username: [{bcolors.OKCYAN}" + username_value + f"{bcolors.ENDC}]")
                print(f" [{bcolors.OKGREEN}>{bcolors.ENDC}] 🔑 Password: [{bcolors.OKCYAN}" + decrypted_password + f"{bcolors.ENDC}]")
                print("----------------------------------")
        
        conn.close()
        os.remove(temp_login_data_path)
        return 0
        
    except sqlite3.Error as e:
        print(f"| [{bcolors.FAIL}x{bcolors.ENDC}] SQL error: {e}")
        return 1

#===========================#

def main():

    if os.name == 'nt':

        try:
            local_state_path = find_local_state()
            login_data_path = find_login_data()

            encrypted_key = get_encrypted_key(local_state_path)
            decryption_key = decrypt_key(encrypted_key)

            login_data_parser(login_data_path, decryption_key)
            
        except Exception as e:
        
            print(f"| [{bcolors.FAIL}x{bcolors.ENDC}] Google Chrome is not installed, or another error occurred: "+str(e))
            
    else:
        print(f"| [{bcolors.FAIL}x{bcolors.ENDC}] This program only runs on Windows systems.")

#===========================#

if __name__ == "__main__":
    main()
