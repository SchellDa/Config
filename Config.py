#!/usb/bin/python
import os,sys
from ConfigParser import ConfigParser

class CfgHandler(ConfigParser):

    def __init__(self, parDict = None):
        self.__prs = ConfigParser()
        self.__prmtr = None     
        if parDict is not None:
            self.init(parDict)
            
    def __cfgExists(self):
        return os.path.exists(self.__cfg)
    
    def init(self, fullDict):        

        if isinstance(fullDict,dict):
        #TODO: Check if val of key is dict
            self.__prmtr = fullDict
            
    def getDict(self, sec):
        
        if self.__prmtr is not None:
        # TODO Try-Except
            return self.__prmtr[sec]
        # sys.exit("Section: %s not defined" %sec)
        
    def getParameters(self):
        return self.__prmtr

    def get(self, sec, par):
        
        if self.__prmtr is not None:
            return self.__prmtr[sec][par]
            
            
    def write(self, fName='config.cfg'):

        with open(fName,'w') as cfgFile:
            if self.__prmtr is not None:
                for sec in self.__prmtr:
                    self.__prs.add_section(sec)
                    for key in self.__prmtr[sec]:
                        self.__prs.set(sec,key,self.__prmtr[sec][key])
            self.__prs.write(cfgFile)

            
    def loadCfg(self,cfg='config.cfg'):

        self.__prmtr = {}
        tmpDict = {}

        # TODO: Create folder
        
        self.__prs.read(cfg)
        for sec in self.__prs.sections():
            for (key,val) in self.__prs.items(sec):
                tmpDict[key] = val
            self.__prmtr[sec] = tmpDict 

            
if __name__ == '__main__':        

    write = False
    
    pDict = {'General':{'vad_file':'VAD',
                        'vdd_file':'VDD',
                        't_file':'temperature',
                        'path':'/mnt/1-wire/honeywell/'},
             'Special':{'d':4,
                        'e':5,
                        'f':6}}

    cfg = CfgHandler()
    
    if write:
        cfg.init(pDict)        
        cfg.write()
    else:
        cfg.loadCfg("config.cfg")
        
    print cfg.get("General","path")
