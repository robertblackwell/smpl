import subprocess
import sys

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

output = ""
result = subprocess.Popen(["ls", "-al", "../project_pig"], stdout=subprocess.PIPE)
while True:
    stdout_line  = result.stdout.readline()
    if not stdout_line:
        break
    line = stdout_line.decode("utf-8") 
    sys.stdout.write(line)
    output += line

result.stdout.close()
return_code = result.wait()
print("got return code")
sys.stdout.write(output)
print("after duplicate output")
# doit(["ls", "-al", "../project_pig/vendor/include/openssl"])