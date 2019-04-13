# core.logs
# by inoro

### CLASSES ####################################################################
class bcolor:
    NONE = ''
    INFO = ''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class p:
    def info(txt):      print(bcolor.INFO       + "[INFO] " + txt + bcolor.ENDC)
    def sinfo(txt):     print(bcolor.HEADER     + "[INFO] " + txt + bcolor.ENDC)
    def ok(txt):        print(bcolor.OKGREEN    + "[ OK ] " + txt + bcolor.ENDC)
    def warning(txt):   print(bcolor.WARNING    + "[WARN] " + txt + bcolor.ENDC)
    def fail(txt):      print(bcolor.FAIL       + "[FAIL] " + txt + bcolor.ENDC)
    def exit(txt):      print(bcolor.OKBLUE     + "[EXIT] " + txt + bcolor.ENDC)
    def loop(txt):      print(bcolor.OKBLUE     + "[LOOP] " + txt + bcolor.ENDC)
    def cin(txt):       print(bcolor.INFO       + "[ <--] " + txt + bcolor.ENDC)
    def cout(txt):      print(bcolor.INFO       + "[--> ] " + txt + bcolor.ENDC)
    def sslcin(txt):    print(bcolor.INFO       + "[ <~~] " + txt + bcolor.ENDC)
    def sslcout(txt):   print(bcolor.INFO       + "[~~> ] " + txt + bcolor.ENDC)
