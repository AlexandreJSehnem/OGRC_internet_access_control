from pysnmp.hlapi import *

# SNMP easy access class


class snMPP:
    target_ip = ''
    target_port = ''
    read_comm = ''
    write_comm = ''
    # __init__
    # @param target_ip : Switch's IP
    # @param target_port : Switch's SNMP port
    # @param read_comm : Read community
    # @param wirte_comm : Write community

    def __init__(self, target_ip: str = '10.90.90.90', target_port: int = 161, read_comm: str = 'public', write_comm: str = "private"):
        self.target_ip = target_ip
        self.target_port = target_port
        self.read_comm = read_comm
        self. write_comm = write_comm
        pass

    # GET
    # @param OID : OID as string
    # Except prints error indication
    # return OID value
    def get(self, OID: str):
        identity = ObjectIdentity('')
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(
                self.read_comm, mpModel=0),
                UdpTransportTarget(
                (self.target_ip, self.target_port)),
                ContextData(),
                ObjectType(ObjectIdentity(OID)))
        )

        if errorIndication:
            print(errorIndication)

        else:
            return varBinds

    # SET
    # @param OID : OID as string
    # @param value : Integer value (does not work otherwise)
    # return NULL
    def set(self, OID: str, value: int):
        types = [int, str]
        for t in types:
            if isinstance(value, int):
                value = Integer(value=value)
            elif isinstance(value, str):
                value = OctetString(value=value)

        g = setCmd(SnmpEngine(),
                   CommunityData(self.write_comm),
                   UdpTransportTarget((self.target_ip, self.target_port)),
                   ContextData(),
                   ObjectType(ObjectIdentity(
                       OID), value)
                   )
        next(g)
