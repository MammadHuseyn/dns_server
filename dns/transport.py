import socket
import struct
from .constants import DNS_PORT, UDP_MAX_SIZE, FLAG_QR

def send_query(data, server, port=DNS_PORT, timeout = 5.0):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(timeout)
        sock.sendto(data,(server, port))
        while True:
            pack, addr = sock.recvfrom(UDP_MAX_SIZE)
            if addr == (server, port):
                return pack


def check_response(query, response):
    if len(response)< 12:
        raise ValueError('Too short to be response')
    
    q_id = struct.unpack('>H', query[:2])[0]
    res_id = struct.unpack('>H', response[:2])[0]

    flag = struct.unpack('>H', response[2:4])[0]
    
    if q_id != res_id  or not flag & FLAG_QR:
        raise ValueError('IDs mismatch or not a response')

    

    