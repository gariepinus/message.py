#!/usr/bin/python
"""
################################################################################
# message.py
#   [Output and log management]
#
# by gariepinus <mail@gariepinus.de>
#  & fleaz <mail@fleaz.me>
#  & evilet <mail@markusschader.de>
################################################################################
"""
import time
import sys

VERSION = "0.2"
LEVELS = ['debug', 'info', 'warning', 'error', 'quiet']


class Message:
    def __init__(self, logfile="", print_level="debug", log_level="info", timeformat="%Y-%m-%d %H:%M:%S",
                 stderror=False, print_time=False):
        """setup message.py, check if given values are valid, check if log accessible"""

        self.timeformat = timeformat
        self.stderr = stderror
        self.print_time = print_time

        log_error = False
        print_error = False
        no_file = False

        if log_level in LEVELS:
            self.log_level = log_level
        else:
            log_error = True
            self.log_level = "info"

        if print_level in LEVELS:
            self.print_level = print_level
        else:
            print_error = True
            self.print_level = "debug"

        if logfile == "" and self.log_level != "quiet":
            self.file_path = "./message_log_" + self.__timestamp().replace(" ", "_")
            no_file = True
        else:
            self.file_path = logfile

        # if loglevel is not quiet: make sure log can be written
        if self.log_level != "quiet":

            # try to access log
            try:
                f = open(self.file_path, "a")
                f.close()
            except IOError as e:
                self.log_level = "quiet"
                self.error("Logfile <{}> not accessible. Switching to loglevel <quiet>.".format(self.file_path),
                           "message.py")

            # warn if loglevel was not valid
            if log_error:
                self.warning("Unkown loglevel. Defaulting to <info>.", "message.py")

            # inform if default logfile is beeing used
            if no_file:
                self.info("No logfile path. Defaulting to <{}>".format(self.file_path), "message.py")

        if print_error:
            self.warning("<{}> is unkown printlevel. Defaulting to <debug>.".format(print_level), "message.py")

        self.debug("READY :: {}".format({"logfile": self.file_path, "print_level": self.print_level,
                                         "log_level": self.log_level, "timeformat": self.timeformat,
                                         "stderror": self.stderr, "print_time": self.print_time}), "message.py")

    def __build(self, message_level, message_text, message_source=None):
        """build message"""

        # build message string
        if message_source:
            message_source = "** {} ** ".format(message_source)
        else:
            message_source = ""

        message = "[{: ^7}] {}{}\n".format(message_level.upper(), message_source, message_text)

        # print message if printlevel not quiet and >= message level
        if self.print_level != "quiet" and self.__levelcheck(message_level, self.print_level):
            self.__print_output(message_level, message)

        # write message to log if loglevel not quiet and >= message level
        if self.log_level != "quiet" and self.__levelcheck(message_level, self.log_level):
            self.__log_output(message)

    def __print_output(self, message_level, message):
        """print message to stdout or stderr"""

        if self.print_time:
            message = "{} {}".format(self.__timestamp(), message)

        if message_level in ["error", "warning"] or self.stderr:
            sys.stderr.write(message)
        else:
            sys.stdout.write(message)

    def __log_output(self, message):
        """write message to logfile"""

        message = "{} {}".format(self.__timestamp(), message)
        # try to access log
        try:
            with open(self.file_path, "a") as f:
                f.write(message)
        except IOError as e:
            self.log_level = "quiet"
            self.error("Logfile <{}> not accessible. Switching to loglevel <quiet>.".format(self.file_path),
                       "message.py")

    @staticmethod
    def __levelcheck(message_level, level):
        """compare message level to print- or loglevel"""

        if LEVELS.index(message_level) >= LEVELS.index(level):
            return True
        else:
            return False

    def __timestamp(self):
        """return timestamp string in choosen format"""
        return time.strftime(self.timeformat)

    def error(self, message, message_source=None):
        """print/log error message"""
        self.__build("error", message, message_source)

    def warning(self, message, message_source=None):
        """print/log warning message"""
        self.__build("warning", message, message_source);

    def info(self, message, message_source=None):
        """print/log info message"""
        self.__build("info", message, message_source);

    def debug(self, message, message_source=None):
        """print/log debug message"""
        self.__build("debug", message, message_source);

## eof
