
### IMPORTS ####################################################################
import socket
import ssl
import base64
import datetime

### GLOBAL VARIABLES ###########################################################
subject = b'Esto es una prueba3'
text = b'LOLOLOLOLO3'
host = 'smtp.gmail.com'
bhost = host.encode('utf-8')
port = 25

with open('cred.txt') as f: cred = f.read()
credarr = cred.split('::')
us = credarr[0].encode('utf-8')
ps = credarr[1].replace('\n','').encode('utf-8')

mailfrom = us
with open('mailto.txt') as f: mailto = f.read()
mailto = mailto.replace('\n','').encode('utf-8')

### FUNCTIONS ##################################################################
def by_b64(by):
    b64 = base64.b64encode(by)
    return b64

def mysend(sock, sdata, expected):
    print('[--> ] ', repr(sdata))
    sock.sendall(sdata)
    rdata = sock.recv(1024)
    print('[ <--] ', repr(rdata))
    if rdata.decode("utf-8")[:3] != expected:
        print('[FAIL] '+expected+' reply not received from server')

def mysslsend(sslsock, sdata, expected):
    print('[~~> ] ', repr(sdata))
    sslsock.sendall(sdata)
    rdata = sslsock.recv(1024)
    print('[ <~~] ', repr(rdata))
    if rdata.decode("utf-8")[:3] != expected:
        print('[FAIL] '+expected+' reply not received from server')

def mysslonlysend(sslsock, sdata):
    print('[~~> ] ', repr(sdata))
    sslsock.sendall(sdata)

### EXEC #######################################################################
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

rdata = sock.recv(1024)
print('[ <--] ', str(rdata))
if rdata.decode("utf-8")[:3] != '220':
    print('[FAIL] 220 reply not received from server')

mysend(sock,b'EHLO '+bhost+b'\r\n','250')
mysend(sock,b'STARTTLS\r\n','220')

sslsock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_SSLv23)

mysslsend(sslsock, b'AUTH LOGIN ' + by_b64(us) + b'\r\n','334')
mysslsend(sslsock, by_b64(ps) + b'\r\n','235')
mysslsend(sslsock, b'MAIL FROM: <' + mailfrom + b'>\r\n','250')
mysslsend(sslsock, b'RCPT TO: <' + mailto + b'>\r\n','250')
mysslsend(sslsock, b'DATA\r\n','354')

now = datetime.datetime.now()
bnow = now.strftime("%a, %d %b %Y %H:%M:%S -0700 (PDT)").encode('utf-8')
mysslonlysend(sslsock, b'Date: ' + bnow + b'\r\n')
mysslonlysend(sslsock, b'From: ' + mailfrom + b'\r\n')
mysslonlysend(sslsock, b'Subject: ' + subject + b'\r\n')
mysslonlysend(sslsock, b'\r\n')
mysslonlysend(sslsock, text + b'\r\n')
mysslonlysend(sslsock, b'.\r\n')

mysslsend(sslsock, b'QUIT\r\n','250')

sslsock.close()
sock.close()
