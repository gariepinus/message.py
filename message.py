#!/usr/bin/python
"""Output and log management"""
version="0.1"


################################################################################
# message.py
#   [Output and log mamagement]
#
# by gariepinus <mail@gariepinus.de>
################################################################################


import time
import sys

log    = ""
printl = ""
logl   = ""
tform  = ""
strerr = False
ptime  = False
ready  = False
levels = set(['debug', 'info', 'warning', 'error', 'quiet'])



def timestamp ():
    """return timestamp string in choosen format"""
    global tform
    return time.strftime(tform)



def setup (logfile = "", printlevel = "debug", loglevel = "info", timeformat = "%Y-%m-%d %H:%M:%S", stderror = False, time = False):
    """setup message.py, check if given values are valid, check if log accessible"""
    global ready,tform,stderr,ptime,levels,logl,printl,log
    ready = True # set readieness true

    tform  = timeformat
    stderr = stderror
    ptime  = time

    logerror   = False
    printerror = False
    nofile     = False

    if (loglevel in levels):
        logl  = loglevel
    else:
        logerror = True
        logl = "info"


    if (printlevel in levels):
        printl = printlevel
    else:
        printerror = True
        logl = "debug"

        
    if (logfile == "" and logl != "quiet"):
        log = "~/message_log_" + timestamp().replace(" ", "_")
        #log = "~/message_log_" + time.strftime("%Y%m%d")
        nofile = True
    else:
        log = logfile


    ### if loglevel is not quiet: make sure log can be written ###
    if (logl != "quiet"):

        # set loglevel to quiet for now
        loglsave = logl
        logl     = "quiet"
        logfail  = False


        # warn if loglevel was not valid
        if (logerror):
            warning("<" + loglevel + "> is unkown loglevel. Defaulting to <info>.","message.py")

        # inform if default log is beeing used
        if (nofile):
            warning("No logfile path. Defaulting to <" + log + ">","message.py")


        # try to access log
        try:
            f = open(log, "a")
            f.close()
        except IOError as e:
            error("Logfile <" + log +  "> not accessible. Switching to loglevel <quiet>.","message.py")
            logfail = True


        if not (logfail):
            # if log is accessible, restore saved loglevel
            logl = loglsave


    if (printerror):
        warning("<" + printlevel + "> is unkown printlevel. Defaulting to <debug>.","message.py")
        
    return 0



def check ():
    """check readiness, call setup with default values if not ready"""
    global ready
    if not (ready):
        setup()
        warning("message.py not configured. Using defaults.","message.py")



def build ( mlevel, message, msgtype=""):
    """build message"""

    global levels,printl,logl

    # make sure we are ready to print/log
    check()

    # check if message has valid level
    if not (mlevel in levels):
        error("Unkown message level: <" + mlevel + "> for <" + message +">.", "message.py")
        return 1


    # build message string
    msg = "[" + mlevel.upper().center(7) + "] :: "

    if (msgtype != ""):
        msg = msg + "**" + msgtype + "** " 

    msg =  msg + message + "\n"


    # print message if printlevel not quiet and >= message level
    if (printl != "quiet" and levelcheck(mlevel, printl)):
        output( mlevel, msg)

    # write message to log if loglevel not quiet and >= message level
    if (logl != "quiet" and levelcheck(mlevel, logl)):
        logwrite(msg)

    return 0



def output(mlevel, message):
    """print message to stdout or stderr"""

    global ptime,stderr

    if (ptime):
        message = timestamp()+ " " + message

    if (mlevel == "error" or mlevel == "warning" or stderr):
        sys.stderr.write(message)
    else:
        sys.stdout.write(message)


def logwrite(message):
    """write message to logfile"""

    global log

    message = timestamp() + " " + message

    # try to access log
    try:
        f = open(log, "a")
        f.write(message)
        f.close()
    except IOError as e:
        logl = "quiet"
        error("Logfile <" + log +  "> not accessible. Switching to loglevel <quiet>.","message.py")

    return 0



def levelcheck (mlevel, level):
    """compare message level to print- or loglevel"""

    if (level == "debug"):
        return True
    if (level == "info" and mlevel != "debug"):
        return True
    if (level == "warn" and mlevel != "debug" and mlevel != "info"):
        return True
    if (level == "error" and mlevel == "error"):
        return True

    return False



def error(message, mtype=""):
    """print/log error message"""
    build( "error", message, mtype);


def warning(message, mtype=""):
    """print/log warning message"""
    build( "warning", message, mtype);


def info(message, mtype=""):
    """print/log info message"""
    build( "info", message, mtype);


def debug(message, mtype=""):
    """print/log debug message"""
    build( "debug", message, mtype);
