from pysnmp.hlapi import *

g = setCmd(SnmpEngine(),
           CommunityData('private'),
           UdpTransportTarget(('10.90.90.90', 161)),
           ContextData(),
           ObjectType(ObjectIdentity(
               '1.3.6.1.2.1.2.2.1.7.5'), Integer(value=1))
           )
next(g)
