
import os

def mem_info():
    return os.popen( "free -m | awk 'NR==2{print $7}'").read()