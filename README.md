# Secure Multiparty Chat

We have created a group chat with end-to-end encryption in CTR mode. The private keys for identity verification are protected with passwords that are genereated by the scrypt key derivation function to thwart dictionary attacks. The group key is generated by the chat inviter and transported securely using the ISO-11770-3/2 protocol. The messages are further protected from replay attacks with sequence numbers that are maintained in a database for all chat participants. Feel free to look through our [design doc](https://github.com/eutopi/Secure-Multiparty-Chat/blob/master/Design_Document.pdf) for more details about our implementation.

## Installation
Install the [PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/src/introduction.html) dependency:
```
pip install pycryptodome
```

## Usage

**New Participants**

When creating new participants, run the following. This generates RSA key pairs for *n* people (in our example case, we have three, but feel free to try as many as you want) and saves them to password-protected files. Enter passwords for each as prompted and make sure you remember these. You will use them later. 
```
python setup/setup.py -n 3
```

**New Chatroom**

Open up five separate terminals. Two will be used to run the network and the server in the background, while three will be acting as the chat client for each participant. That is, run in the following order:
```
1. python netsim/network.py -a 'SABC' -c (S = server, ABC = participants)
2. python netsim/server.py
3. python main.py -s B (-s refers to self, so this is the client for participant B)
4. python main.py -s C (this is the client for participant C)
5. python main.py -s A -i (this is the client for participant A. -i designates A to the group chat inviter)
```
*Note: make sure steps (3) and (4) have reached the* ```Main loop started...``` *prompt before you run step (5). This is because B and C need to be waiting for the server in order to receive what is sent by A.*

Now, key exchange will occur and send/receive sequence numbers for all the participants be will reset. When you see the prompt ```Begin chatting!```, everything is ready and you can type into the terminal and have a secure conversation!
