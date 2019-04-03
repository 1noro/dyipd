# modules.ip
# by inoro

### IMPORTS ####################################################################
import os
import socket
import re

### FUNCTIONS ##################################################################
def mysend(sock, sdata, expected, verbose):
    if verbose >= 3: print('[--> ] ', repr(sdata))
    sock.sendall(sdata)
    rdata = sock.recv(1024)
    if verbose >= 3: print('[ <--] ', repr(rdata))
    if rdata.decode("utf-8")[:3] != expected:
        print('[FAIL] '+expected+' reply not received from server')
    return rdata

def get_my_ip_from_gmail(verbose):
    myip = ''
    host = 'smtp.gmail.com'
    bhost = host.encode('utf-8')
    port = 25
    if verbose >= 2: print("[INFO] getting my ip from "+host+":"+str(port))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    rdata = sock.recv(1024)
    if verbose >= 3: print('[ <--] ', str(rdata))
    if rdata.decode("utf-8")[:3] != '220':
        print('[FAIL] 220 reply not received from server')
    ehlo_rdata = mysend(sock, b'EHLO '+bhost+b'\r\n', '250', verbose)
    rdata = mysend(sock, b'QUIT\r\n', '221', verbose)
    sock.close()

    regex = re.compile(r'\[(.*)\]')
    myip = regex.search(ehlo_rdata.decode('utf-8'))[1]
    return myip

def check_ip(file, verbose):
    myip = ''
    mylastip = ''
    myip_change = False

    if os.path.isfile(file):
        with open(file) as f: ipraw = f.read()
        mylastip = ipraw.replace('\n','')
        if verbose >= 1: print("[INFO] last ip: "+mylastip)
        ip_from_gmail = get_my_ip_from_gmail(verbose)
        if verbose >= 2: print("[INFO] ip from gmail: "+ip_from_gmail)
        if mylastip != ip_from_gmail:
            myip_change = True
            myip = ip_from_gmail
            if verbose >= 1: print("[INFO] the ip has changed to: "+myip)
            f = open(file, "w+")
            f.write(myip+"\n")
            f.close()
            if verbose >= 2: print("[INFO] '"+file+"' saved with the new ip")
        else:
            myip = mylastip
            if verbose >= 1: print("[INFO] the ip has not changed")
    else:
        myip_change = True
        print("[WARN] '"+file+"' not found, creating one...")
        ip_from_gmail = get_my_ip_from_gmail(verbose)
        if verbose >= 2: print("[INFO] ip from gmail: "+ip_from_gmail)
        myip = ip_from_gmail
        if verbose >= 1: print("[INFO] the new ip is: "+myip)
        f = open(file, "w+")
        f.write(myip+"\n")
        f.close()
        if verbose >= 2: print("[INFO] '"+file+"' saved with the new ip")

    return (myip, myip_change)
