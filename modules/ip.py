# modules.ip
# by inoro

### IMPORTS ####################################################################
import os
import socket
import re

import core.log as log

### FUNCTIONS ##################################################################
def mysend(sock, sdata, expected, verbose):
    if verbose >= 3: print('[--> ] ', repr(sdata))
    sock.sendall(sdata)
    rdata = sock.recv(1024)
    if verbose >= 3: print('[ <--] ', repr(rdata))
    if rdata.decode("utf-8")[:3] != expected:
        log.p.fail(expected+' reply not received from server')
    return rdata

def get_my_ip_from_gmail(verbose):
    myip = ''
    host = 'smtp.gmail.com'
    bhost = host.encode('utf-8')
    port = 25
    if verbose >= 2: log.p.info("getting my ip from "+host+":"+str(port))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    rdata = sock.recv(1024)
    if verbose >= 3: print('[ <--] ', str(rdata))
    if rdata.decode("utf-8")[:3] != '220':
        log.p.fail('220 reply not received from server')
    ehlo_rdata = mysend(sock, b'EHLO '+bhost+b'\r\n', '250', verbose)
    rdata = mysend(sock, b'QUIT\r\n', '221', verbose)
    sock.close()

    regex = re.compile(r'\[(.*)\]')
    # print(regex.search(ehlo_rdata.decode('utf-8')).group(1))
    myip = regex.search(ehlo_rdata.decode('utf-8')).group(1)
    return myip

def check_ip(file, verbose):
    myip = ''
    mylastip = ''
    myip_change = False

    if os.path.isfile(file):
        with open(file) as f: ipraw = f.read()
        mylastip = ipraw.replace('\n','')
        if verbose >= 1: log.p.info("last ip: "+mylastip)
        ip_from_gmail = get_my_ip_from_gmail(verbose)
        if verbose >= 2: log.p.info("ip from gmail: "+ip_from_gmail)
        if mylastip != ip_from_gmail:
            myip_change = True
            myip = ip_from_gmail
            if verbose >= 1: log.p.info("the ip has changed to: "+myip)
            f = open(file, "w+")
            f.write(myip+"\n")
            f.close()
            if verbose >= 2: log.p.info("'"+file+"' saved with the new ip")
        else:
            myip = mylastip
            if verbose >= 1: log.p.info("the ip hasn't changed")
    else:
        myip_change = True
        log.p.warning("'"+file+"' not found, creating one...")
        ip_from_gmail = get_my_ip_from_gmail(verbose)
        if verbose >= 2: log.p.info("ip from gmail: "+ip_from_gmail)
        myip = ip_from_gmail
        if verbose >= 1: log.p.info("the new ip is: "+myip)
        f = open(file, "w+")
        f.write(myip+"\n")
        f.close()
        if verbose >= 2: log.p.info("'"+file+"' saved with the new ip")

    return (myip, myip_change)
