import os
import json
import logging
from collections import OrderedDict

class Config(object):
    """ Class that converts json based config files into dictonaries

    The ConfigParser class is used to parse JSON based config files.
    This small program is mainly used in the context of KITPlot and other
    scipts developed in the hardware group of the ETP at KIT.

    """

    def __init__(self,cfg=None):
        """ Initialize ConfigHandler by loading the config file.

        The __init__ method sets the working directory to ./cfg and loads the
        config file.

        Args:
            cfg (str): The config file that is loaded

        """
        self.__dir = ""
        self.__fName = ""
        self.__cfg = {}

        self.__setupLogger()

        if cfg is not None:
            self.load(cfg)

    def __getitem__(self,keys):
        try:
            return self.__cfg[keys]
        except:
            pass

        try:
            return self.__getFromDict(self.__cfg,keys)
        except:
            raise KeyError("Key not found")


    def __setitem__(self, key, value):
        """ Set or change a value of a new or existing parameter

        Args:
            key (dict): List of keys with unlimited levels
            value (): Value that will be set

        """

        self.__setInDict(self.__cfg,key,value)
        self.write(self.__fName)

    def __setupLogger(self):
        self.__log = logging.getLogger(__name__)
        self.__log.setLevel(logging.DEBUG)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.DEBUG)

        consoleFormatter = logging.Formatter('%(levelname)s - %(message)s')
        consoleHandler.setFormatter(consoleFormatter)

        self.__log.addHandler(consoleHandler)

    def setDir(self,directory='cfg/'):
        """ Set the working directory

        Args:
            directory (str): Working directory where the config files are
                located

        """

        if directory[-1] is not "/":
            directory+="/"

        self.__dir = os.getcwd() + "/" + directory


    def load(self, cfg='default.cfg'):
        """ Load config file

        Args:
            cfg (str): Name of cfg file inside the working directory

        """

        if self.__dir is "":
            #self.__fName = os.path.dirname(os.path.abspath(__file__)) + "/" + cfg
            self.__fName = os.getcwd() + "/" + cfg
        else:
            self.__fName = self.getfName(cfg)

        self.__log.debug("Config filepath: {0}".format(self.__fName))

        try:
            with open(self.__dir + self.__fName) as cfgFile:
                self.__cfg = json.load(cfgFile, object_pairs_hook=OrderedDict)
        except:
            raise OSError("No file found")

    def write(self, cfg='default.cfg'):

        try:
            if not os.path.exists(self.__dir):
                os.makedirs(self.__dir)
        except:
            pass

        with open(self.__dir + cfg, 'w') as cfgFile:
            json.dump(self.__cfg, cfgFile, indent=4, sort_keys=True)

    def setConfig(self, dictionary):
        """ Sets the dictionary manually

        Args:
            dictionary
        """
        if not isinstance(dictionary, dict):
            raise TypeError("{0} is not a dictionary".format(dictionary))

        self.__cfg = dictionary

    # Get a given data from a dictionary with position provided as a list
    def __getFromDict(self, dataDict, mapList):
        for k in mapList: dataDict = dataDict[k]
        return dataDict

    # Set a given data in a dictionary with position provided as a list
    def __setInDict(self, dataDict, mapList, value):
        for k in mapList[:-1]: dataDict = dataDict[k]
        dataDict[mapList[-1]] = value


    def __getfName(self, name='default'):
        if os.path.isdir(str(name)):
            return os.path.normpath(str(name)).split("/")[-1] + ".cfg"
        else:
            return os.path.splitext(os.path.basename(
                        os.path.normpath(str(name))))[0] + ".cfg"

if __name__ == '__main__':

    testDict = { "a": "1",
                 "b": "2",
                 "c":
                 { "d": "3",
                   "e": "4"}}

    cfg = Config()
    cfg.setDir("cfg")
    cfg.setConfig(testDict)
    cfg.write()
