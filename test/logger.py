"""
##########################################################
# logger - A class module to assist you in your logging. #
#                                                        #
# This is a stand alone logging function file.           #
# It gives you an ease creating logging functionality    #
# for your test cases. This only depends upon the        #
# modules we import                                      #
##########################################################
"""

# Standard Python Libraries
import os
import logging
from datetime import datetime

class Logger():
    """ Custom logger"""

    def __init__(self, propagate=True, loglevel=20):
        """
        Descriptions -
            Constructor for Logger which initializes all variables.

        Mandatory Args -
            None

        Optional Args -
            propagate (bool) : True (default) - Propagate log level across
                               False - Don't propagate log level
            loglevel (int)   : 20 (default) - INFO
                               10 - DEBUG
                               30 - WARNING
                               40 - ERROR
                               50 - CRITICAL

        Usage -
            >>> from logger import Logger ; log = Logger(__file__)
        """
        # Default log msg format
        self.msg_format = '%(asctime)s | %(levelname).4s | %(lineno)-4d | %(module)-20s | %(message)s'

        # Default log date format
        self.date_format = '%m/%d/%y %H:%M:%S'

        # Default log directory
        self.log_dir = "logs"

        # Create the log directory if it does not exists
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Log level
        self.loglevel = loglevel

        # File Handle
        self.file_handle = None

        # Enable / Disable Propagation
        self.propagate = propagate

        # Enable formatter
        self.formatter = logging.Formatter(fmt=self.msg_format, datefmt=self.date_format)

        # Define log instance
        self.log = logging.getLogger('root')

        # Assume we have no stream handlers
        found = False

        # Find if we have any instance of stream handler
        for each in list(logging.root.handlers):
            each = str(each)

            if each.split(" ")[0].split(".")[1] == "StreamHandler":
                found = True
                break

        # If not found create one
        if not found:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            self.log.root.addHandler(console_handler)

    def file_logger(self, name, propagate=True):
        """
        Descriptions -
            Create a testcase logger which enables file logging

        Mandatory Args -
            name (str) : File name

        Optional Args -
            propagate (bool) : True (default) - Propagate log level across
                               False - Don't propagate log level
        Usage -
            >>> from logger import Logger ; log = Logger(__file__).testcase()
        """
        # Fetch the name of logger
        name = os.path.basename(name).split('.')[0]

        # Get a child logger from root for testcase
        self.log = logging.getLogger(name).getChild("root.testcase")

        # Set the logging to required level
        self.log.setLevel(self.loglevel)

        # Enable or Disable Propagation
        self.propagate = propagate

        # Assume we have no file handlers
        found = False

        # Find if there is already a file logger
        for each in list(logging.root.handlers):
            each = str(each)
            if each.split(" ")[0] == "FileHandler":
                found = True
                break

        # If not found create one
        if not found:
            file_suffix = datetime.now().strftime('%b_%d_%y_%H_%M_%S')
            file_handle = logging.FileHandler(self.log_dir + '/' + name + '_' + file_suffix + '.log')
            file_handle.setFormatter(self.formatter)
            self.log.root.addHandler(file_handle)
            self.file_handle = file_handle

        return self.log
