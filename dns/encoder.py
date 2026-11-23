import struct
from .constants import MAX_LABEL_LEN, MAX_NAME_LEN, RecordClass, RecordType
from .message import Header, Question, Message
import secrets

def encode_header(header):
    return struct.pack(
        '>6H',
        header.q_id,
        header.flags(),
        header.qdcount,
        header.ancount,
        header.nscount,
        header.arcount,
    )


def encode_name(name: str):
    name = name.removesuffix('.')
    res = bytearray()
    if name=="":
        return b'\x00'
    
    for i in name.split("."):
        if not i:
            raise ValueError('DNS name contains empty label.')

        encoded_label = i.encode('ascii')

        if len(encoded_label)>MAX_LABEL_LEN:
            raise ValueError('Name label is too long.')
        
        res.append(len(encoded_label))
        res.extend(encoded_label)
    res.append(0)

    if len(res) > MAX_NAME_LEN:
            raise ValueError('DNS address is too long.')
    return bytes(res)


def encode_question(question):
    return encode_name(question.qname) + struct.pack(
        '>2H',
        question.qtype,
        question.qclass,
    )

def encode_message(message):
    message.header.qdcount = len(message.questions)
    res = encode_header(message.header)
    for question in message.questions:
        res += encode_question(question)

    return res

def build_query(name, qtype=RecordType.A, qclass=RecordClass.IN, recursion_desired=True, query_id=None):
    if query_id is None:
        query_id = secrets.randbelow(65536)
    header = Header(query_id, rd=recursion_desired)
    question = Question(qname=name, qtype=qtype, qclass=qclass)
    message = Message(header, [question])
    return message
