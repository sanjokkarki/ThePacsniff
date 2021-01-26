"""
  The real stuff. 
"""

import socket,sys,struct

# create a network socket using the default constructor
try:
  sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
except socket.error:
  print('Socket could not be created.')
  sys.exit(1)

def get_mac_address(bytesString):
  bytesString = map('{:02x}'.format, bytesString)
  destination_mac = ':'.join(bytesString).upper()
  return destination_mac

# while loop runs infinitely to capture any incoming packets
while True:

  # listen on port 65565
  raw_data, address = sock.recvfrom(65565)
  destination_mac, src_mac, ethernet_proto = struct.unpack('! 6s 6s H', raw_data[:14])

  # packet parameters
  destination_mac = get_mac_address(destination_mac)
  src_mac = get_mac_address(src_mac)
  ethernet_proto = socket.htons(ethernet_proto)
  data = raw_data[14:]

  print('\nEthernet frame:')
  print('\tDestination: {}, Source: {}, Ethernet Protocol: {}'.format(destination_mac, src_mac, ethernet_proto))

   # analyse only IPv4 packets (I know IPv6 is the real deal but this should work for now)
  if (ethernet_proto == 8):
    version_header_len = data[0]
    version = version_header_len >> 4
    header_len = (version_header_len & 15) * 4
    ttl,proto,src,target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])

    src = '.'.join(map(str,src)) 
    target = '.'.join(map(str,target)) 
    
    print('IPv4 packet:')
    print('\tVersion: {}, Header length: {}, TTL: {}'.format(version,header_len,ttl))
    print('\tProtocol: {}, Source: {}, Target: {}'.format(proto,src,target))
