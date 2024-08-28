#===========================#
# I M P O R T S             #
#===========================#

import base64
import os
import win32api
import win32con
import win32gui
import win32ui

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

def getDimensions():

    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    
    return (width, height, left, top)

#===========================#

def screenshot(name='screenshot.bmp'):

    hdesktop = win32gui.GetDesktopWindow()
    width, height, left, top = getDimensions()
    
    desktopDC = win32gui.GetWindowDC(hdesktop)
    imgDC = win32ui.CreateDCFromHandle(desktopDC)
    memDC = imgDC.CreateCompatibleDC()
    
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(imgDC, width, height)
    memDC.SelectObject(screenshot)
    memDC.BitBlt((0,0), (width, height), imgDC, (left, top), win32con.SRCCOPY)
    screenshot.SaveBitmapFile(memDC, f'{name}')
    
    memDC.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())
    
    print(f"[{bcolors.OKGREEN}>{bcolors.ENDC}] Screenshot taken: [{bcolors.OKCYAN}"+name+f"{bcolors.ENDC}]")

#===========================#

def run():

    screenshot()
    with open('screenshot.bmp') as f:
        img = f.read()
    return img

#===========================#

if __name__ == '__main__':

    screenshot()