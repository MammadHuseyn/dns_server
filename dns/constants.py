from enum import IntEnum

#https://datatracker.ietf.org/doc/html/rfc1035#section-3.2.2

#https://datatracker.ietf.org/doc/html/rfc1035#section-4.1.1


class RecordType(IntEnum):
    A = 1
    NS = 2
    CNAME = 5
    SOA = 6
    NULL = 10
    WKS = 11
    HINFO = 13
    MINFO = 14
    MX = 15
    TXT = 16
    AAAA = 28 #RFC 3596

class QueryType(IntEnum):
    AXFR = 252
    MAILB = 253
    ANY = 255

class RecordClass(IntEnum):
    IN = 1 #internet
    CH = 3 #chaos
    HS = 4 #hesiod

class Opcode(IntEnum):
    QUERY = 0
    IQUERY = 1
    STATUS = 2

class Rcode(IntEnum):
    NOERROR = 0
    FORMATERROR = 1
    SERVERFAIL = 2
    NAMEERROR = 3
    NOIMP = 4
    REFUSED = 5


FLAG_QR = 0x8000
FLAG_AA = 0x0400
FLAG_TC = 0x0200
FLAG_RD = 0x0100
FLAG_RA = 0x0080

OPCODE_SHIFT = 11 #(flags >> 11) & 0xF
RCODE_MASK = 0x000F #flags & 0xF

MAX_LABEL_LEN = 63
MAX_NAME_LEN = 255
UDP_MAX_SIZE = 512
DNS_PORT = 53