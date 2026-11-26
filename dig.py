import sys
import argparse
import struct

from dns.encoder import build_query, encode_message
from dns.transport import send_query, check_response
from dns.constants import FLAG_AA, FLAG_QR, FLAG_RA, FLAG_RD, FLAG_TC, RCODE_MASK, OPCODE_SHIFT, Rcode




if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('domain')
    parser.add_argument('q_id', nargs='?', type = int, default=None)
    args = parser.parse_args()

    query = encode_message(build_query(name = args.domain, query_id=args.q_id))

    response = send_query(query, "8.8.8.8")
    check_response(query, response)

    q_id, flags, qdcount, ancount, nscount, arcount = struct.unpack(">6H", response[:12])

    #flags
    qr = bool(flags & FLAG_QR)
    aa = bool(flags & FLAG_AA)
    tc = bool(flags & FLAG_TC)
    rd = bool(flags & FLAG_RD)
    ra = bool(flags & FLAG_RA)

    opcode = (flags >> OPCODE_SHIFT) & 0xF
    rcode_num = flags & RCODE_MASK

    try:
        rcode_name = Rcode(rcode_num).name
    except:
        raise ValueError('Rcode name error')

    print(f"ID:      {q_id:#06x} ({q_id})")
    print(f"Flags:   {flags} (QR={int(qr)}, Opcode={opcode}, AA={int(aa)}, TC={int(tc)}, RD={int(rd)}, RA={int(ra)}, RCODE={rcode_name})")
    print(f"QDCOUNT: {qdcount}")
    print(f"ANCOUNT: {ancount}")
    print(f"NSCOUNT: {nscount}")
    print(f"ARCOUNT: {arcount}")

    #ans_name, ans_type, ans_class, ttl, rdlen, rdata  = struct.unpack('>HHHIHI', response[32:48])
    #print(ans_name, ans_type, ans_class, ttl, rdlen, rdata)

    """
    bytes	hex	field	meaning
    32-33	c00c	NAME	compression pointer → name at byte 12 (see below)
    34-35	0001	TYPE	A
    36-37	0001	CLASS	IN
    38-41	00000214	TTL	532 seconds the answer can be cached (4 bytes!)
    42-43	0004	RDLENGTH	the data is 4 bytes long
    44-47	08080808	RDATA	8.8.8.8
    """


"""
 15 | 14 13 12 11 | 10 | 9  | 8  | 7  | 6 5 4 | 3 2 1 0
 QR |   Opcode    | AA | TC | RD | RA |   Z   |  RCODE
"""

"""header
    bytes	hex	field	meaning
    0-1	0016	ID	22, the same as the query ✔
    2-3	8080	FLAGS	QR = 1 (response), RA = 1
    4-5	0001	QDCOUNT	1 question
    6-7	0002	ANCOUNT	2 answers
    8-9	0000	NSCOUNT	0
    10-11	0000	ARCOUNT	0
"""
    