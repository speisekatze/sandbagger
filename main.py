# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 23:37:56 2015

@author: n4p
"""

import time
from src.httpServer import http_request
from src.httpServer import http_server
from src.config import Config


conf = Config(filename="sandbagger.conf")


Handler = http_request.HttpRequest
HTTPD = http_server.HttpServer(Handler, int(conf.value("Server/port")))
HTTPD.set_cert(conf.value("Server/cert"), conf.value("Server/key"))
HTTPD.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Server shutting down")
HTTPD.stop()
