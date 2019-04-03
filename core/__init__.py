# core.__init__
# by inoro

### IMPORTS ####################################################################
import sys
import os

import core
from core import utils

import modules
from modules import ip
from modules import ddns
from modules import mail

### EDITABLE VARIABLES #########################################################
TABULAR = " "*8
DDNS_FILE = "data/namecheap-data.txt"
MAILFROM_FILE = "data/mailfrom.txt"
MAILSTO_FILE = "data/mailsto.txt"
LASTIP_FILE = "data/lastip.txt"

### AUTOMATIC VARIABLES ########################################################
verbose = 0
sendmail = False
domains = []
mailfrom_user = b''
mailfrom_pass = b''
mailfrom_mail = b''
mailsto = []
myip = ''
myip_change = False

### NON EDITABLE VARIABLES #####################################################

### MAIN #######################################################################
def main():
    # --- Parameters -----------------------------------------------------------
    (options, args) = utils.options_definition()
    # --- verbose
    verbose = int(options.verbose)
    # --- sendmail
    sendmail = options.sendmail

    # --- CHECK CONFIG ---------------------------------------------------------
    # --- DDNS_FILE
    if os.path.isfile(DDNS_FILE):
        domains = utils.compose_domains(DDNS_FILE)
    else:
        print("[FAIL] '"+DDNS_FILE+"' not found")
        sys.exit()

    if verbose >= 2: utils.list_configured_domains(domains, TABULAR)

    # --- MAILFROM_FILE
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

        if verbose >= 2:
            print("[INFO] configured mailfrom: "+mailfrom_mail.decode('utf-8'))

    # --- MAILSTO_FILE
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

        if verbose >= 2: utils.list_mailsto(mailsto, TABULAR)

    # --- CHECK IP -------------------------------------------------------------
    (myip, myip_change) = ip.check_ip(LASTIP_FILE, verbose)

    # --- UPDATE DDNS ----------------------------------------------------------
    if myip_change: ddns.update(domains, verbose)
