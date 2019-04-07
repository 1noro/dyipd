# modules.mail
# by inoro

### IMPORTS ####################################################################
import socket
import ssl
import base64
import datetime

import core.log as log

### FUNCTIONS ##################################################################
def by_b64(by):
    b64 = base64.b64encode(by)
    return b64

def mysend(sock, sdata, expected, verbose):
    if verbose >= 3: log.p.cout(repr(sdata))
    sock.sendall(sdata)
    rdata = sock.recv(1024)
    if verbose >= 3: log.p.cin(repr(rdata))
    if rdata.decode("utf-8")[:3] != expected:
        log.p.fail(expected+' reply not received from server')

def mysslsend(sslsock, sdata, expected, verbose):
    if verbose >= 3: log.p.sslcout(repr(sdata))
    sslsock.sendall(sdata)
    rdata = sslsock.recv(1024)
    if verbose >= 3: log.p.sslcin(repr(rdata))
    if rdata.decode("utf-8")[:3] != expected:
        log.p.fail(expected+' reply not received from server')

def mysslonlysend(sslsock, sdata, verbose):
    if verbose >= 3: log.p.sslcout(repr(sdata))
    sslsock.sendall(sdata)

def send(us, ps, mailfrom, mailsto, myip, mylastip, verbose):
    host = 'smtp.gmail.com'
    bhost = host.encode('utf-8')
    port = 25
    subject = "[DYIP] New IP ("+myip+")"
    bsubject = subject.encode('utf-8')
    if mylastip != '':
        text = "Your dynamic IP has changed from "+mylastip+" to "+myip+"."
    else:
        text = "Your dynamic IP has changed to "+myip+"."
    btext = text.encode('utf-8')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    rdata = sock.recv(1024)
    if verbose >= 3: log.p.cin(str(rdata))
    if rdata.decode("utf-8")[:3] != '220':
        log.p.fail('220 reply not received from server')

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
