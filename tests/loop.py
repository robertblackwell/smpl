import sys
import os
import time

for k in [1,2,3,4,5,6,7,8,9,0]:
    for m in [1,2,3,4,5,6,7,8,9,0]:
        print("This is instance k = {} m = {} abcdefghijklmnopqrstuvwxyz ".format(k, m))
    time.sleep(1)

sys.stderr.write("This is to stderr\n")
sys.stderr.write("This is to stderr\n")    
sys.stderr.write("This is to stderr\n")    
sys.stderr.write("This is to stderr\n")    
sys.stderr.write("This is to stderr\n")
sys.stderr.write("This is to stderr\n")
sys.stderr.write("This is to stderr\n")    
sys.stderr.write("This is to stderr\n")    
sys.stderr.write("This is to stderr\n")    
sys.stderr.write("This is to stderr\n")
sys.exit(42)