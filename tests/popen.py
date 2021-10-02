import subprocess
import sys
import os
from typing import List
LisOfString = List[str]

import termcolor as TC

TC.cprint("Attention", "cyan", attrs=["bold"])
txt = "{}:{}:{}".format(
    TC.colored("This is the first bit", "magenta"), 
    TC.colored("the second bit", "cyan", attrs=['bold']), 
    TC.colored("the third bit", "green", attrs=['bold']))
print(txt)
# for stdout_line in iter(popen.stdout.readline, ""):
# 	yield stdout_line
# popen.stdout.close()


def doit(cmd):
	print("in try_popen")
    # result = subprocess.Popen(["ifconfig"], stdout=PIPE)
	# result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    # return_code = result.wait()
    # print(return_code)
	# if return_code:
	# 	raise subprocess.CalledProcessError(return_code, cmd)

def doit1(cmd):
    print("hello world")

def stream_it(thing):
    while True:
        stdout_line  = thing.readline()
        if not stdout_line:
            break
        line = stdout_line.decode("utf-8") 
        sys.stdout.write(line)

def popen_exec(cmd: List[str]):
    output: str = ""
    try:
        result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stream_it(result.stdout)
        # while True:
        #     stdout_line  = result.stdout.readline()
        #     if not stdout_line:
        #         break
        #     line = stdout_line.decode("utf-8") 
        #     sys.stdout.write(line)
        #     output += line

        result.stdout.close()
        return_code: int = result.wait()
        if return_code != 0:
            x = result.stderr
            # print(t.bold_red_on_black('We got a bad return code : ') + t.bold_green(str(return_code)) )
            stream_it(x)
            # print("We got a bad  error_code : {}".format(return_code))
            # while True:
            #     err_line = result.stderr.readline()
            #     if not err_line:
            #         break
            #     eline = err_line.decode("utf-8")
            #     sys.stderr.write(eline)

    except Exception as exception:
        print ("An exception occurred while running command [{}] error type: " +type(exception).__name__ + " {}".format(cmd, str(exception)))
        quit()

# doit(["ls", "-al", "../project_pig/vendor/include/openssl"])
cwd = os.getcwd()
loop = os.path.join(cwd, "loop.py")
cmd = ["/usr/bin/python3", loop]
print('We got a bad return code : ')

popen_exec(cmd)