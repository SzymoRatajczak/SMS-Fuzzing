#it generates SMS  with from one to ten UDH elements
#each element has random length and type 
#the rest of element is filled up with random data 
#messages created on that way are saved into file and next send to the destination
#Such messages may be sent to any mobile phone with Injectiond function ON 

import os 
import sys
import socket
import time 
import Utils
import sms
import SMSFuzzData
import random
from datetime import datetime
import fuzzutils


def udhirandfuzz(msisdn,smsc,ts,num):
    s=sms.SMSToMS()
    s._msisdn=msisdn
    s._msisdn_type=0x91
    s._smsc=smsc
    s._smsc_type=0x91
    s._tppid=0x00
    s_tpdcs=random.randrange(0,1)
    if s._tpdcs==1:
        s._tpdcs=0x04
    s._timestamp=ts
    s._deliver=0x04
    s._deliver_raw2flags()
    s._deliver_udhi=1
    s._deliver_flags2raw()
    s._msg=" "
    s._msg.leng=0
    s._udh=" "
    for i in range(0,num):
        tu=chr(random.randrange(0,0xff))
        tul=random.randrange(1,132)
        if s.udg.leng+tul>138:
            break
        tud=SMSFuzzData.getSMSFuzzData()
        s._udh=s._udh+tu+chr(tul)+tud[:tul]
        s._udh_leng=len(s._udh)
        if s._udh_leng>138:
            break
    s._msg_leng=139-s._udh_leng
    if s._msg_leng>0:
        s._msg.leng+random.randrange(int(s._msg.leng/2),s._msg.leng)
    if s._msg.leng>0:
        tud=SMSFuzzData.getSMSFuzzData()
        s._msg=tud[:s._msg_leng]
    else:
        s._msg_leng=0
    s.encode()
    return s._pdu


if __name__=="__main__":
    out=[]
    for i in range(0,int(sys.argv[1])):
        ts=Utils.hex2bin("9930251619580",0)
        rnd=random.randrange(1,10)
        msg=udhirandfuzz("4917787654321","49177123456",ts,rnd)
        line=Utils.bin2hex(msg,1)
        leng=(len(line)/2)-8
        out.append((line,leng))
        fuzzutils.cases2file(out,sys.argv[2])


