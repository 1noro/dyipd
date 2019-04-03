# modules.ddns
# by inoro

### IMPORTS ####################################################################
import socket

import xml.etree.ElementTree as ET

### FUNCTIONS ##################################################################
def namecheap_http_update(web, verbose):
    out = False
    host = 'dynamicdns.park-your-domain.com'
    bhost = host.encode('utf-8')
    port = 80
    bweb = web.encode('utf-8')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    sdata = b'GET /' + bweb + b' HTTP/1.1\r\n'
    if verbose == 3: print('[--> ] ', repr(sdata))
    sock.sendall(sdata)
    sdata = b'Host: ' + bhost + b'\r\n'
    if verbose == 3: print('[--> ] ', repr(sdata))
    sock.sendall(sdata)
    sdata = b'\r\n'
    if verbose == 3: print('[--> ] ', repr(sdata))
    sock.sendall(sdata)
    rdata = sock.recv(1024)
    sock.close()
    if verbose == 3: print('[ <--] ', repr(rdata))

    rdataarr = rdata.decode("utf-8").split('\r\n')
    expected = 'HTTP/1.1 200 OK'
    if rdataarr[0] != expected:
            print('[FAIL] "'+expected+'" reply not received from server')
    xml_tree = ET.fromstring(rdataarr[len(rdataarr)-1])
    if (xml_tree.find('Done').text == 'true'):
        out = True
    else:
        print('[FAIL] operation not "Done"')

    return out

def update(domains, verbose):
    if verbose == 1: print("[INFO] updating ip in the dynamic dns")
    for domain in domains:
        for dhost in domain["hosts"]:
            web = 'update?domain='+domain["dname"]+'&password='+domain["dpass"]+'&host='+dhost
            if namecheap_http_update(web, verbose):
                if verbose == 1: print('[ OK ] '+dhost+'.'+domain["dname"])
            else:
                if verbose == 1: print('[FAIL] '+dhost+'.'+domain["dname"])
