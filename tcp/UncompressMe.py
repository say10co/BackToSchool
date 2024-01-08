import socket, zlib, base64,re
from socket import AF_INET, SOCK_STREAM

def decompress(zlib_b):
    return (zlib.decompress(zlib_b))

def decode64(b64_str):
    return (base64.b64decode(b64_str))

def read_and_send_answer(sock):
    while True:
        data = sock.recv(1024).decode('UTF-8')
        match = re.search("'(.*)'", data)
        if (not match):
            match = re.search('^.* flag: (.+)$',  data)
            print(match.group(1))
            break
        zlib_b64 = match.group(1)
        # decode base64 
        b64_decoded = decode64(zlib_b64)
        # decompress data using zlib
        zlib_decompressed = decompress(b64_decoded)
        print(zlib_decompressed)
        sock.send(zlib_decompressed + b'\n')

def solve(address, port):
    sock = socket.socket(AF_INET, SOCK_STREAM)
    sock.connect((address, port))
    read_and_send_answer(sock)
    sock.close()

solve("challenge01.root-me.org", 52022)

