#!/usr/bin/env python3
#invite.py

from netsim.netinterface import network_interface
from Crypto.Signature import PKCS1_PSS
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from datetime import datetime

'''
    Time = 17 bytes
    Cipher = 128 bytes (content = 1 byte (ID) and 16 bytes (public key))
    Signature = length varies, index at i=145 until the end
'''

# Can change these specifications later
INVITER_ID = 'A'
INVITEE_LIST = 'BC'
GROUP_ID = 0

def invite(netif, INVITER_ID, INVITEE_LIST, GROUP_ID, password):
    print('Inviter is ' + INVITER_ID)
    print('Invitees are ' + INVITEE_LIST)
    print('Group id is ' + str(GROUP_ID))
    time = datetime.now()
    print('The current time is ' + str(time))
    timestamp = datetime.timestamp(time)
    print('The timestamp is ' + str(timestamp))
    if len(str(timestamp)) != 17:
        timestamp = str(timestamp) + '0'
    groupkey = get_random_bytes(16)
    print('Generating group key...' + str(groupkey))

    # RSA PKCS1 PSS SIGNATURE
    # import the private key of inviter

    sigkfile = open("setup/%s-key.pem"%INVITER_ID,'r')
    sigkeystr = sigkfile.read()
    sigkfile.close()
    sigkey = RSA.import_key(sigkeystr,passphrase = password)
    signer = PKCS1_PSS.new(sigkey)

    #NET_PATH = './netsim/network/'
    OWN_ADDR = INVITER_ID
    # ISO 11770-3/2
    #netif = network_interface(NET_PATH, OWN_ADDR)
    print('Invite loop started...')
    for invitee in INVITEE_LIST:
        
        #print('Encryption started...')
        
        # import public key of invitee for RSA
        pubkeystr = ''
        with open('setup/table%s.txt'%OWN_ADDR) as f:
            kfile = f.read()
        pubkeys = kfile.split("member:")
        pubkeys.pop(0)
        for k in pubkeys:
            if k[0] == invitee:
                pubkeystr = k.split("key:")[1]
        if(pubkeystr == ''):
            print('No public key string read!')
            exit(1)

        #print('(pubkeystr):' + pubkeystr)

        
        plaintext = INVITER_ID.encode('utf-8') + str(GROUP_ID).encode('utf-8') + groupkey
        # Public key encryption using RSA
        pubkey = RSA.import_key(pubkeystr)
        cipher = PKCS1_OAEP.new(pubkey)
        ciphertext = cipher.encrypt(plaintext)
        #print('Encryption complete.')
        
        #print('Signing for ' + invitee + '...')
        msg_to_be_signed = (invitee + str(timestamp)).encode('utf-8') + ciphertext
        h = SHA256.new()
        h.update(msg_to_be_signed)
        signature = signer.sign(h)
        #print('Signature complete.')
        
        msg = str(timestamp).encode('utf-8') + ciphertext + signature
        #print(msg)

        # Send the encrypted message
        netif.send_msg('S', msg)
        print('Invitation to ' + invitee + ' sent.');
        status, msg = netif.receive_msg(blocking=True)
    return groupkey
