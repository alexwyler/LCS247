'''
Created on Sep 14, 2014

@author: alexwyler
'''
import collections
import configparser

CONFIG_FILE_PATH = "config.properties"
CONTEXT_UTIL = collections.OrderedDict()

def init_sction_map( section, config ):
    options = config.options(section)
    for option in options:
        try:
            CONTEXT_UTIL[option] = config.get(section, option)
        except:
            print("exception on %s!" % option)

def init():
    config = configparser.ConfigParser()
    config.read( CONFIG_FILE_PATH )
    for section in config.sections():
        init_sction_map(section, config)
    print("Config finished initializing...")


# if __name__ == "__main__":
#     init();
#    USAGE: CONTEXT_UTIL['ahk_path']