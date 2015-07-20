#!/usr/bin/env python3

import socket
import os
import random
from socket import inet_ntoa
from struct import pack

client_port = 68
server_port = 67

""" DHCP Message format rfc2131
"""

op = b'\x01'
htype = b'\x01'
hlen = b'\x06'
hops = b'\x00'
xid = pack('!L', (random.getrandbits(32)))
secs = b'\x00\x00'
flags = b'\x80\x00'
ciadd = pack('!4s', b'\x00')
yiaddr = pack('!4s', b'\x00')
siaddr = pack('!4s', b'\x00')
giaddr = pack('!4s', b'\x00') 
chaddr = pack('!6B', 0x00, 0x0c, 0x29, 0x61, 0x02, 0x21)
chaddr_pad = pack('!10s', b'\x00')
sname = pack('!64s', b'\x00')
bname = pack('!128s', b'\x00')
cookie = pack('!4B', 0x63, 0x82, 0x53, 0x63)

"""  Options rfc2132
"""

mtype = pack('!3B', 53, 1, 1)
cident = pack('!12B', 61, 10, 68, 72, 67, 80, 67, 108, 105, 101, 110, 116) 
request = pack('!3B', 55, 1, 1)
end = pack('!B', 255)

dmessage = op + htype + hlen + hops + xid + secs + flags + ciadd + yiaddr +\
           siaddr + giaddr + chaddr + chaddr_pad + sname + bname + cookie +\
           mtype + cident + request + end

def main():
    if os.getuid():
        print("Must be run as Root")
        exit()
    print("Sending DHCP Discover")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(('0.0.0.0', client_port))
    s.sendto(dmessage, ('<broadcast>', server_port))
    
    while True:
        data = s.recvfrom(1024)
        print("Offer recieved from:", data[1][0], "IP Offered:", inet_ntoa(data[0][16:20]))

if __name__ == '__main__':
    main()
