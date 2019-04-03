# utils.__init__
# by inoro

### IMPORTS ####################################################################
from optparse import OptionParser

### EDITABLE VARIABLES #########################################################


### AUTOMATIC VARIABLES ########################################################

### NON EDITABLE VARIABLES #####################################################
verbose = False
background = False
sendmail = False

### FUNCTIONS ##################################################################

### MAIN #######################################################################
def main():
    # --- Parameters -----------------------------------------------------------
    parser = OptionParser()
    parser.add_option(
        "-v", "--verbose", dest="verbose",
        action="store_true", default=False,
        help="print status messages to stdout.")
    parser.add_option(
        "-b", "--background", dest="background",
        action="store_true", default=False,
        help="starts dypd in background mode.")
    parser.add_option(
        "-m", "--sendmail", dest="sendmail",
        action="store_true", default=False,
        help="send a mail when dynamic ip changes.")

    (options, args) = parser.parse_args()

    # --- verbose
    verbose = options.verbose
    # --- background
    background = options.background
    # --- sendmail
    sendmail = options.sendmail

    print(verbose, background, sendmail)
