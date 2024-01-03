import codecs, string
import socket, re

def lib_rot13_decode(string):
    decoded = codecs.decode(string, 'rot_13')
    return (decoded)

#: Decode Rot13  encoded string 
def rot13_decode(rot_13):
    rot13_chain = list(string.ascii_lowercase + string.ascii_lowercase)
    decoded =  ""
    for c in rot_13:
        if (not c.isalpha()):
            decoded = decoded + c
            continue
        if (c.islower()):
            decoded = decoded + rot13_chain[rot13_chain.index(c) + 13]
        else:
            decoded = decoded + rot13_chain[rot13_chain.index(c.lower()) + 13].upper()
    return (decoded)


def  validate():
    host =  "challenge01.root-me.org"
    port =  52021
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    received_data = sock.recv(1024)
    match = re.search(".*'(\w+)'.*$", received_data.decode('UTF-8'))
    rot13_encoded = match.group(1)
    rot13_decoded = lib_rot13_decode(rot13_encoded)  

    sock.send((rot13_decoded+ "\n").encode())

    # gets flag on success !!
    print(sock.recv(1024))

validate()

