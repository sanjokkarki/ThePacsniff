"""
  This is the barebones structure of a packet sniffer
  The idea is to create your own socket and make it listen
  to incoming traffic on a particular port
  This program will just log the gibberish (which is actually hexadecimal data)
  that it reads from the received packets.
"""
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

while True:
  print(s.recvfrom(65565))
  