#===========================#
# I M P O R T S             #
#===========================#

import datetime
import os
import shutil
import time
from urllib.parse import urlparse
from pathlib import Path
import splinter

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

def take_screenshot(url, filename, name=None, headless=True, width=None, height=None, wait=None):

    if name is None:
        now = datetime.datetime.now()
        date_time = now.isoformat().split(".")[0]
        name = f"{date_time}-{urlparse(url).netloc}-"
        
    print(f"| [{bcolors.OKGREEN}>{bcolors.ENDC}] Creating browser object...")
        
    browser = splinter.Browser("chrome", headless=headless)
    
    print(f"")
    print(f"| [{bcolors.OKGREEN}>{bcolors.ENDC}] Setting window dimensions...")
    
    if width is not None and height is not None:
        browser.driver.set_window_size(width, height)
        
    print(f"| [{bcolors.OKGREEN}>{bcolors.ENDC}] Visiting URL: [{bcolors.WARNING}"+url+f"{bcolors.ENDC}]...")
        
    browser.visit(url)
    
    if wait is not None:
        time.sleep(wait)
        
    print(f"| [{bcolors.OKGREEN}>{bcolors.ENDC}] Taking screenshot...")
    
    browser.driver.save_screenshot(str(filename))
    
    print(f"| [{bcolors.OKGREEN}>{bcolors.ENDC}] Took screenshot: [{bcolors.WARNING}"+filename+f"{bcolors.ENDC}].")
    
    browser.quit()

#===========================#

def main():

    filename = "TestScreenshot.png"

    take_screenshot("https://google.com", filename)

#===========================#

if __name__ == "__main__":

    main()