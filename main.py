# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 23:37:56 2015

@author: n4p
"""

from lib import *
from lib.httpServer import *
import time
import sys

conf = Config.Config('Config/sandbagger.conf')

handler = httpRequest.httpRequest
handler.externHandler = RequestHandler.RequestHandler(conf)
httpd = httpServer.httpServer(handler,int(conf.value('Server/port')))

httpd.start()
time.sleep(600)
httpd.stop()

