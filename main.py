# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 23:37:56 2015

@author: n4p
"""

from lib import *
from lib.httpServer import *
import time
import sys
import keyboard

conf = Config.Config('Config/sandbagger.conf')

handler = httpRequest.httpRequest
handler.externHandler = RequestHandler.RequestHandler(conf)
httpd = httpServer.httpServer(handler,int(conf.value('Server/port')))

httpd.start()
print('Press "q" to stop Server.')
while True:
    try:
        time.sleep(1)
        if keyboard.is_pressed('q'):
            print('Shutting Down!')
            break
    except:
        print(sys.exc_info()[0]) 
        break

httpd.stop()

