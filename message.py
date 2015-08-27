#!/usr/bin/python
"""
################################################################################
# message.py
#   [Output and log management]
#
# by gariepinus <mail@gariepinus.de>
################################################################################
"""
version="0.1"


import time
import sys


def timestamp ():
    """return timestamp string in choosen format"""
    global tform
    return time.strftime(tform)


class message:
    def __init__ (self,logfile = "", printlevel = "debug", loglevel = "info", timeformat = "%Y-%m-%d %H:%M:%S", stderror = False, time = False):
        """setup message.py, check if given values are valid, check if log accessible"""

        self.levels = set(['debug', 'info', 'warning', 'error', 'quiet'])

        self.tform  = timeformat
        self.stderr = stderror
        self.ptime  = time

        logerror   = False
        printerror = False
        nofile     = False


        if (loglevel in levels):
            self.logl  = loglevel
        else:
            logerror = True
            self.logl = "info"


        if (printlevel in levels):
            self.printl = printlevel
        else:
            printerror = True
            self.logl = "debug"

        
        if (logfile == "" and logl != "quiet"):
            self.log = "~/message_log_" + timestamp().replace(" ", "_")
            nofile = True
        else:
            self.log = logfile


        ### if loglevel is not quiet: make sure log can be written ###
        if (self.logl != "quiet"):

            # set loglevel to quiet for now
            loglsave = self.logl
            self.logl     = "quiet"
            logfail  = False


            # warn if loglevel was not valid
            if (logerror):
                self.warning("<" + loglevel + "> is unkown loglevel. Defaulting to <info>.","message.py")

            # inform if default log is beeing used
            if (nofile):
                self.warning("No logfile path. Defaulting to <" + log + ">","message.py")


            # try to access log
            try:
                f = open(self.log, "a")
                f.close()
            except IOError as e:
                self.error("Logfile <" + self.log +  "> not accessible. Switching to loglevel <quiet>.","message.py")
                logfail = True


            if not (logfail):
                # if log is accessible, restore saved loglevel
                self.logl = loglsave


            if (printerror):
                warning("<" + printlevel + "> is unkown printlevel. Defaulting to <debug>.","message.py")
        
        return 0


    def build ( mlevel, message, msgtype=""):
        """build message"""

        # check if message has valid level
        if not (mlevel in self.levels):
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

        if (ptime):
            message = self.timestamp()+ " " + message

        if (mlevel == "error" or mlevel == "warning" or self.stderr):
            sys.stderr.write(message)
        else:
            sys.stdout.write(message)


    def logwrite(message):
        """write message to logfile"""

        message = timestamp() + " " + message

        # try to access log
        try:
            f = open(self.log, "a")
            f.write(message)
            f.close()
        except IOError as e:
            self.logl = "quiet"
            error("Logfile <" + self.log +  "> not accessible. Switching to loglevel <quiet>.","message.py")

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
        seldbuild( "error", message, mtype);


    def warning(message, mtype=""):
        """print/log warning message"""
        build( "warning", message, mtype);


def info(message, mtype=""):
    """print/log info message"""
    build( "info", message, mtype);


def debug(message, mtype=""):
    """print/log debug message"""
    build( "debug", message, mtype);
