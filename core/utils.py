# core.utils
# by inoro

### IMPORTS ####################################################################
import datetime

from optparse import OptionParser

import core.log as log

### FUNCTIONS ##################################################################
def options_definition():
    parser = OptionParser()
    parser.add_option(
        "-v", "--verbose", dest="verbose",
        help="print status messages to stdout. There are 3 levels of detail.",
        metavar="LEVEL")
    parser.add_option(
        "-m", "--sendmail", dest="sendmail",
        action="store_true", default=False,
        help="send a mail when dynamic ip changes.")
    parser.add_option(
        "-l", "--loop", dest="loop",
        action="store_true", default=False,
        help="run the program in a loop.")
    return parser.parse_args()

def compose_domains(file):
    out = []
    with open(file) as f: ncdata = f.read()
    ncdata_rows = ncdata.split('\n')
    domain_row = True
    domain_num = 0
    for row in ncdata_rows:
        if domain_row and (row != ''):
            drarr = row.split('::')
            out.append({
                "dname":drarr[0],
                "dpass":drarr[1],
                "hosts":[]
            })
            domain_row = False
        elif (row != ''):
            out[domain_num]["hosts"].append(row)
        elif (row == ''):
            domain_row = True
            domain_num += 1
    return out

def list_configured_domains(domains, t):
    log.p.info("configured domains:")
    str = ""
    for d in domains:
        str = d["dname"]+" ( "
        for h in d["hosts"]:
            str += h+" "
        str += ")"
        print(t+str)

def list_mailsto(mailsto, t):
    log.p.info("configured mails to notify:")
    for m in mailsto:
        print(t+m.decode('utf-8'))

def get_new_strtime():
    now = datetime.datetime.now()
    strnow = now.strftime("%Y-%m-%d %H:%M:%S")
    return strnow
