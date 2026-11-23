from .constants import *

class Header:
    def __init__(self, q_id , qr=False, opcode=Opcode.QUERY, 
                 aa=False, tc=False, rd=True, ra=False, rcode=Rcode.NOERROR,
                 qdcount=0, ancount=0, nscount=0, arcount=0 ):
        self.q_id = q_id
        self.qr = qr
        self.opcode = opcode
        self.aa = aa
        self.tc = tc
        self.rd = rd
        self.ra = ra
        self.rcode = rcode
        self.qdcount = qdcount
        self.ancount = ancount
        self.nscount = nscount
        self.arcount = arcount

    def __repr__(self):
        return (f'ID: {self.q_id}\nQR: {self.qr}, Opcode: {self.opcode}\n'
                f'AA: {self.aa}, TC: {self.tc}, RD: {self.rd}, RA: {self.ra}, Rcode: {self.rcode}\n'
                f'QDCount: {self.qdcount}, ANCount: {self.ancount}, NSCount: {self.nscount}, ARCount: {self.arcount}')
    
    def flags(self):
        res = 0
        if self.qr:
            res |= FLAG_QR
        res |= self.opcode << OPCODE_SHIFT
        if self.aa:
            res |= FLAG_AA
        if self.tc:
            res |= FLAG_TC
        if self.rd:
            res |= FLAG_RD
        if self.ra:
            res |= FLAG_RA
        res |= self.rcode & RCODE_MASK
        return res


class Question:
    def __init__(self, qname: str, qtype=RecordType.A, qclass=RecordClass.IN):
        self.qname = qname
        self.qtype = qtype
        self.qclass = qclass

    def __repr__(self):
        return (f'QName: {self.qname}, QType: {self.qtype}, QClass: {self.qclass}')

class Message():
    def __init__(self, header: Header, questions=None):
        self.header = header
        self.questions = list(questions) if questions is not None else []




if __name__ == '__main__':
    print(hex(Header(22, qdcount=1).flags()))                     # 0x100
    print(hex(Header(1, rd=False).flags()))                       # 0x0
    print(hex(Header(1, qr=True, ra=True).flags()))               # 0x8180
    print(hex(Header(1, qr=True, rcode=Rcode.NAMEERROR).flags())) # 0x8103

    m1 = Message(Header(1))
    m2 = Message(Header(2))
    m1.questions.append(Question("a.com"))
    print(len(m1.questions))

    m = Message(Header(1))
    m.questions.append(Question("a.com"))
    print(m.header.qdcount)

