#Sends message to 'Injectord' function on mobile phone
#Injectord is listenning on TCP port no.4242 and waiting for +CMT communciat
#this communicat is made of two lines
#first line: length
#second line: message encoded by hex


#first parameter- destination's IP address
#second-message
#third- length of message
#fourth- CRLF character

def sendmsg(dest_ip,msg,msg_cmt,crlftype=1):
    error=0
    if crlftype==1:
        buffor="+CMT:.%d\r\n%s\r\n"%(msg_cmt,msg)
    elif crlftype==2:
        buffor="\n+CMT:%d\n%s\n"%(msg_cmt,msg)
    elif crlftype==3:
           buffor="\n+CMT:.%d\r\n%s\r\n"%(msg_cmt,msg)
    so=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        so.connect((dest_ip,4223))
    except:
        error=1
    try:
        so.send(buffer)
    except:
        error=2
    so.close()
    return error
