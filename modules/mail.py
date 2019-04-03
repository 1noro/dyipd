# modules.mail
# by inoro

### IMPORTS ####################################################################
import socket
import ssl
import base64
import datetime

### FUNCTIONS ##################################################################
def by_b64(by):
    b64 = base64.b64encode(by)
    return b64

def mysend(sock, sdata, expected, verbose):
    if verbose >= 3: print('[--> ] ', repr(sdata))
    sock.sendall(sdata)
    rdata = sock.recv(1024)
    if verbose >= 3: print('[ <--] ', repr(rdata))
    if rdata.decode("utf-8")[:3] != expected:
        print('[FAIL] '+expected+' reply not received from server')

def mysslsend(sslsock, sdata, expected, verbose):
    if verbose >= 3: print('[~~> ] ', repr(sdata))
    sslsock.sendall(sdata)
    rdata = sslsock.recv(1024)
    if verbose >= 3: print('[ <~~] ', repr(rdata))
    if rdata.decode("utf-8")[:3] != expected:
        print('[FAIL] '+expected+' reply not received from server')

def mysslonlysend(sslsock, sdata, verbose):
    if verbose >= 3: print('[~~> ] ', repr(sdata))
    sslsock.sendall(sdata)

def send(us, ps, mailfrom, mailsto, myip, verbose):
    host = 'smtp.gmail.com'
    bhost = host.encode('utf-8')
    port = 25
    subject = "[DYIP] Your dynamic IP has changed to "+myip
    bsubject = subject.encode('utf-8')
    text = "Your dynamic IP has changed to '"+myip+"'."
    btext = text.encode('utf-8')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    rdata = sock.recv(1024)
    if verbose >= 3: print('[ <--] ', str(rdata))
    if rdata.decode("utf-8")[:3] != '220':
        print('[FAIL] 220 reply not received from server')

    mysend(sock,b'EHLO '+bhost+b'\r\n','250', verbose)
    mysend(sock,b'STARTTLS\r\n','220', verbose)

    sslsock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_SSLv23)

    mysslsend(sslsock, b'AUTH LOGIN ' + by_b64(us) + b'\r\n','334', verbose)
    mysslsend(sslsock, by_b64(ps) + b'\r\n','235', verbose)
    mysslsend(sslsock, b'MAIL FROM: <' + mailfrom + b'>\r\n','250', verbose)
    for m in mailsto:
        mysslsend(sslsock, b'RCPT TO: <' + m + b'>\r\n','250', verbose)
    mysslsend(sslsock, b'DATA\r\n','354', verbose)

    now = datetime.datetime.now()
    bnow = now.strftime("%a, %d %b %Y %H:%M:%S -0700 (PDT)").encode('utf-8')
    mysslonlysend(sslsock, b'Date: ' + bnow + b'\r\n', verbose)
    mysslonlysend(sslsock, b'From: ' + mailfrom + b'\r\n', verbose)
    mysslonlysend(sslsock, b'Subject: ' + bsubject + b'\r\n', verbose)
    mysslonlysend(sslsock, b'\r\n', verbose)
    mysslonlysend(sslsock, btext + b'\r\n', verbose)
    mysslonlysend(sslsock, b'.\r\n', verbose)

    mysslsend(sslsock, b'QUIT\r\n','250', verbose)

    sslsock.close()
    sock.close()
