'''
Created on Sep 15, 2014

@author: alexwyler
'''
import datetime

def log(tag, message):
    time = datetime.datetime.now().strftime('%d/%m/%y %I:%M:%S %p %Z')
    
    prefix = '{0} {1}'.format(time.ljust(22, ' '), '[ {0} ]'.format(tag).ljust(13, ' '))
    print('{0}{1}'.format(prefix, message))