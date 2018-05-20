#after injection of SMS  i overview system logs  ( using logcat ADB command)
#If logs have native errors or Java's exceptions ,i will save results in
#logcat command and content of SMS  for this test case
#After each test case i clean system logs and go to the next test case 
#Each 50 messages  entire SMS database will be deleted and program will be restared 

import os 
import time
import socket

def get_log(path=" " ):
    cmd=path+" adb logcat-d"
    l=os.popen(cmd)
    r=l.read()
    l.close()
    return r

def clean_log(path=""):
    cmd=path+"adb logcat-c"
    l=os.popen(cmd)
    r=l.read()
    l.close()
    return r


def check_log(log):
    e=0
    if log.find("Excpetion")!=-1:
        e=1
    if log.find("EXCEPTION")!=-1:
        e=1
    if log.find("exception")!=-1:
        e=1
    return e


def kill_proc(path="", name=""):
    cmd=path+"adb shell\"su -c busybox killall -9"+name+"\""
    l=os.popen(cmd)
    r=l.read()
    l.close()
    return r

def clean_sms_db(path=""):
    cmd=path+"adb shell\"su -c rm"
    cmd=cmd+"/data/data/com.android.providers.telephony"
    cmd=cmd+"/databases/mmssms.db\" "
    l=os.popen(cmd)
    r=l.read()
    l.close()
    return r

def cleanup_device(path=" "):
    clean_sms_db(path)
    kill_proc(path,"com.android.mms")
    kill_proc(path,"com.android.phone")


def log_bug(filename,log,test_case):
    fp=open(filename)
    fp.write(test_case)
    fp.write("\n*--------------------\n")
    fp.write(log)
    fp.write("\n")
    fp.write("\n---------------------*\n")
    fp.close()


def file2cases(filename):
    out=[]
    fp=open(filename)
    line=fp.readline()
    while line:
        cr=line.split(" " )
        out.append((cr[0],int(cr[1].rstrip("\n"))))
        line=fp.readline()
    fp.close()
    return out 


def sendcases(dest_ip,cases,logpath,cmdpath="",crlftype=1,delay=5,status=0,start=0):
    count=0
    cleaner=0
    for i in cases:
        if count>=start:
            (line,cmt)=i
            error=sendmsg(dest_ip,line,cmt,crlftype)
            if status>0:
                print("%d) error=%d data:%s"%(count,error,line))
                time.sleep(delay)
            l=get_log(cmdpath)
            if check_log(l)==1:
                lout=line+ " " + str(cmt)+ " \n\n"
                log_bug(logpath+ str(time.time())+".log",l,lout)
            clean_log(cmdpath)
            count=count+1
            cleaner=cleaner+1
            if cleaner>=50:
                cleanup_device(cmdpath)
                cleaner=0
            
def sendcasesfromfile(filename,dest_ip,cmdpath=" " ,crlftype=1,delay=5,logpath="./logs/",status=0,start=0):
    cases=file2cases(filename)
    sendcases(dest_ip,cases,logpath,cmdpath,crlftype=crlftype,status=status,start=start)

if __name__=="__main__":
      fn=os.sys.argv[1]
      dest=os.sys.argv[2]
      start=0
      if len(os.sys.argv)>3:
          start=int(os.sys.srgv[3])
      print("Sending test cases from %s tp %s"% (fn,dest))
      sendcasesfromfile(fn,dest,cmdpath="",crlftype=3,status=1,start=start)
