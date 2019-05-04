#!/usr/bin/env python3
#invite.py

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from prng.prng import generate
import datetime

INVITER_ID = 'A'
INVITEE_LIST = 'BC'
GROUP_ID = 0

'''
for opt, arg in opts:
    if opt == '-h' or opt == '--help':
        print('Usage: python invite.py -i <inviter id> -g <group id>')
        sys.exit(0)
    elif opt == '-i' or opt == '--id':
        INVITER_ID = arg
    elif opt == '-g' or opt == '--group':
        GROUP_ID = arg
'''

print('Inviter is ' + INVITER_ID)
print('Invitees are' + INVITER_LIST)
print('Group id is ' + GROUP_ID)
time = datetime.datetime.now()
print('The current time is ' + str(time))
groupkey = generate()
print('Generating group key...' + groupkey)

# RSA PKCS1 PSS SIGNATURE
# import the key pair of INVITER_ID
sigkfile = open('signature key file placeholder', 'r')
sigkeystr = kfile.read()
sigkfile.close()
sigkey = RSA.import_key(sigkeystr)
signer = PKCS1_PSS.new(sigkey)

NET_PATH = './network/'
OWN_ADDR = INVITER_ID
netif = network_interface(NET_PATH, OWN_ADDR)
print('Main loop started...')
for invitee in INVITEE_LIST:
    print('Signing for ' + invitee + '...', end='')
    msg_to_be_signed = invitee + GROUP_ID + groupkey + time
    h = SHA256.new()
    h.update(msg_to_be_signed)
    signature = signer.sign(h)

    msg = INVITER_ID + GROUP_ID + groupkey + time + signature

    # Public key encryption using RSA
    kfile = open('rsa pub key of invitee', 'r')
    pubkeystr = kfile.read()
    kfile.close()
    pubkey = RSA.import_key(pubkeystr)
    cipher = PKCS1_OAEP.new(pubkey)
    ciphertext = cipher.encrypt(msg)

    # Send the encrypted message
    print('Sending invitation to ' + invitee);
    netif.send_msg('S', msg.encode('utf-8'))
