#!/usr/bin/env python3
#receiver.py

import os, sys, getopt, time
from netinterface import network_interface

NET_PATH = './network/'
OWN_ADDR = 'S'

# ------------
# main program
# ------------

try:
    opts, args = getopt.getopt(sys.argv[1:], shortopts='hp:a:', longopts=['help', 'path=', 'addr='])
except getopt.GetoptError:
    print('Usage: python server.py -p <network path> -a <own addr>')
    sys.exit(1)

for opt, arg in opts:
    if opt == '-h' or opt == '--help':
        print('Usage: python server.py')
        sys.exit(0)

if (NET_PATH[-1] != '/') and (NET_PATH[-1] != '\\'): NET_PATH += '/'

if not os.access(NET_PATH, os.F_OK):
    print('Error: Cannot access path ' + NET_PATH)
    sys.exit(1)

if len(OWN_ADDR) > 1: OWN_ADDR = OWN_ADDR[0]

if OWN_ADDR not in network_interface.addr_space:
    print('Error: Invalid address ' + OWN_ADDR)
    sys.exit(1)

# main loop
netif = network_interface(NET_PATH, OWN_ADDR)
print('Main loop started...')
while True:
    # Calling receive_msg() in non-blocking mode ...
    #    status, msg = netif.receive_msg(blocking=False)
    #    if status: print(msg)      # if status is True, then a message was returned in msg
    #    else: time.sleep(2)        # otherwise msg is empty
    
    # Calling receive_msg() in blocking mode ...
    status, msg = netif.receive_msg(blocking=True)
    if status:
        print('Received message:')
        print(msg)
        netif.send_msg('ABC', msg)
        print('Sending message:')
        print(msg)

