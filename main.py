# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 23:37:56 2015

@author: n4p
"""

import time
from lib.httpServer import http_request
from lib.httpServer import httpServer
#from lib import request_handler
from lib import config




Handler = http_request.HttpRequest
#Handler.externHandler = request_handler.RequestHandler(CONF)
HTTPD = httpServer.httpServer(Handler, int(config.Config().value('Server/port')))

HTTPD.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt as error:
    print('Server shutting down')
HTTPD.stop()
