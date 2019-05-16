# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 14:38:14 2019

@author: Mah
"""
#SERVER
import socket

s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
port = 1234
server = socket.gethostname()

s.bind((server, port))
s.listen(5)

so, a = s.accept()
print("connection form {} ".format(a))

while True:
    msg = so.recv(2048)
    so.send(msg)
    