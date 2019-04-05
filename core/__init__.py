# core.__init__
# by inoro

### IMPORTS ####################################################################
import sys
import os
import time

import core
from core import utils
from core import log

import modules
from modules import ip
from modules import ddns
from modules import mail

### EDITABLE VARIABLES #########################################################
# 1m = 60s, 5m = 300s, 10m = 600s, 15m = 900s, 30m = 1800s
# 1h = 3600s, 2h = 7200, 5h = 18000s, 12h = 43200s, 24h = 86400s, 48h = 172800s
LOOP_TIME = 300
TABULAR = " "*8
DDNS_FILE = "data/namecheap-data.txt"
MAILFROM_FILE = "data/mailfrom.txt"
MAILSTO_FILE = "data/mailsto.txt"
LASTIP_FILE = "data/lastip.txt"

### AUTOMATIC VARIABLES ########################################################
verbose = 0
sendmail = False
loop = False
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
    verbose = 0
    if options.verbose :
        verbose = int(options.verbose)
    # --- sendmail
    sendmail = options.sendmail
    # --- sendmail
    loop = options.loop

    # --- CHECK CONFIG ---------------------------------------------------------
    # --- DDNS_FILE
    if os.path.isfile(DDNS_FILE):
        domains = utils.compose_domains(DDNS_FILE)
    else:
        log.p.fail("'"+DDNS_FILE+"' not found")
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
            log.p.fail("'"+MAILFROM_FILE+"' not found")
            sys.exit()

        if verbose >= 2:
            log.p.info("configured mailfrom: "+mailfrom_mail.decode('utf-8'))

    # --- MAILSTO_FILE
    if sendmail:
        if os.path.isfile(MAILSTO_FILE):
            with open(MAILSTO_FILE) as f: mailsto_cont = f.read()
            mailstoarr = mailsto_cont.split('\n')
            for m in mailstoarr:
                if (m != ""):
                    mailsto.append(m.encode('utf-8'))
        else:
            log.p.fail("'"+MAILSTO_FILE+"' not found")
            sys.exit()

        if verbose >= 2: utils.list_mailsto(mailsto, TABULAR)

    while True:
        # --- CHECK IP ---------------------------------------------------------
        (myip, myip_change) = ip.check_ip(LASTIP_FILE, verbose)

        # --- UPDATE DDNS ------------------------------------------------------
        if myip_change: ddns.update(domains, verbose)

        # --- NOTIFY VIA EMAIL -------------------------------------------------
        if sendmail and myip_change:
            if verbose >= 1: log.p.info("sending notification email...")
            mail.send(mailfrom_user, mailfrom_pass, mailfrom_mail, mailsto, myip, verbose)

        # --- ENDO OF LOOP CHECK -----------------------------------------------
        if loop:
            if verbose >= 1:
                log.p.loop("end of cycle, waiting for "+str(LOOP_TIME)+" seconds...")
            time.sleep(LOOP_TIME)
        else:
            break

    if verbose >= 1: log.p.exit("end of the execution")
