import subprocess

command = 'source/rpc_server srv1'
print(command)
subprocess.Popen(command, shell = True)