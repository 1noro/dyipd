# utils.__init__
# by inoro

### IMPORTS ####################################################################
import sys
import os

from optparse import OptionParser

### EDITABLE VARIABLES #########################################################
DDNS_FILE = "data/namecheap-data.txt"
MAILFROM_FILE = "data/mailfrom.txt"
MAILSTO_FILE = "data/mailsto.txt"
TABULAR = " "*12

### AUTOMATIC VARIABLES ########################################################
verbose = False
sendmail = False
domains = []
mailfrom_user = b''
mailfrom_pass = b''
mailfrom_mail = b''
mailsto = []

### NON EDITABLE VARIABLES #####################################################

### FUNCTIONS ##################################################################
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

def list_configured_domains(domains):
    print("[INFO] configured domains:")
    str = ""
    for d in domains:
        str = d["dname"]+" ( "
        for h in d["hosts"]:
            str += h+" "
        str += ")"
        print(TABULAR+str)

def list_mailsto(mailsto):
    print("[INFO] configured mails to notify:")
    for m in mailsto:
        print(TABULAR+m.decode('utf-8'))

### MAIN #######################################################################
def main():
    # --- Parameters -----------------------------------------------------------
    parser = OptionParser()
    parser.add_option(
        "-v", "--verbose", dest="verbose",
        action="store_true", default=False,
        help="print status messages to stdout.")
    parser.add_option(
        "-m", "--sendmail", dest="sendmail",
        action="store_true", default=False,
        help="send a mail when dynamic ip changes.")

    (options, args) = parser.parse_args()

    # --- verbose
    verbose = options.verbose
    # --- sendmail
    sendmail = options.sendmail

    # @@@ CHECK CONFIG @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # --- DDNS_FILE ------------------------------------------------------------
    if os.path.isfile(DDNS_FILE):
        domains = compose_domains(DDNS_FILE)
    else:
        print("[FAIL] '"+DDNS_FILE+"' not found")
        sys.exit()

    if verbose: list_configured_domains(domains)

    # --- MAILFROM_FILE --------------------------------------------------------
    if sendmail:
        if os.path.isfile(MAILFROM_FILE):
            with open(MAILFROM_FILE) as f: cred = f.read()
            credarr = cred.split('::')
            mailfrom_user = credarr[0].encode('utf-8')
            mailfrom_pass = credarr[1].replace('\n','').encode('utf-8')
            mailfrom_mail = mailfrom_user
        else:
            print("[FAIL] '"+MAILFROM_FILE+"' not found")
            sys.exit()

        if verbose:
            print("[INFO] configured mailfrom: "+mailfrom_mail.decode('utf-8'))

    # --- MAILSTO_FILE ---------------------------------------------------------
    if sendmail:
        if os.path.isfile(MAILSTO_FILE):
            with open(MAILSTO_FILE) as f: mailsto_cont = f.read()
            mailstoarr = mailsto_cont.split('\n')
            for m in mailstoarr:
                if (m != ""):
                    mailsto.append(m.encode('utf-8'))
        else:
            print("[FAIL] '"+MAILSTO_FILE+"' not found")
            sys.exit()

        if verbose: list_mailsto(mailsto)
