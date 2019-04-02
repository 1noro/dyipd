
### IMPORTS ####################################################################
import socket
import datetime

import xml.etree.ElementTree as ET

### GLOBAL VARIABLES ###########################################################
verbose = False

host = 'dynamicdns.park-your-domain.com'
bhost = host.encode('utf-8')
port = 80

### AUTOMATED VARIABLES ########################################################
domains = []
with open('namecheap-data.txt') as f: ncdata = f.read()
ncdata_rows = ncdata.split('\n')
# print(ncdata_rows)
domain_row = True
domain_num = 0
for row in ncdata_rows:
    if domain_row and (row != ''):
        drarr = row.split('::')
        domains.append({
            "dname":drarr[0],
            "dpass":drarr[1],
            "hosts":[]
        })
        domain_row = False
    elif (row != ''):
        domains[domain_num]["hosts"].append(row)
    elif (row == ''):
        domain_row = True
        domain_num += 1

# print(domains)

### FUNCTIONS ##################################################################
def http_request(web,host,bhost,port):
    out = False
    bweb = web.encode('utf-8')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    sdata = b'GET /' + bweb + b' HTTP/1.0\r\n'
    if verbose: print('[--> ] ', repr(sdata))
    sock.sendall(sdata)
    sdata = b'Host: ' + bhost + b'\r\n'
    if verbose: print('[--> ] ', repr(sdata))
    sock.sendall(sdata)
    sdata = b'\r\n'
    if verbose: print('[--> ] ', repr(sdata))
    sock.sendall(sdata)
    rdata = sock.recv(1024)
    sock.close()
    if verbose: print('[ <--] ', repr(rdata))

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


### EXEC #######################################################################

for domain in domains:
    for dhost in domain["hosts"]:
        web = 'update?domain='+domain["dname"]+'&password='+domain["dpass"]+'&host='+dhost
        if http_request(web,host,bhost,port):
            print('[ OK ] '+dhost+'.'+domain["dname"])
        else:
            print('[FAIL] '+dhost+'.'+domain["dname"])
