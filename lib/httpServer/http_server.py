# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 14:22:28 2015

@author: n4p
"""
__version__ = "0.2"

import socketserver
import ssl
import _thread


class HttpServer:
    """ a simple socketserver based http server with ssl support """

    handler = None
    httpd = None
    port = 0
    cert_filename = ""
    logfile = None

    def __init__(self, handler=None, port=None):
        self.handler = handler
        self.port = port
        self.logfile = open("httpd.log", "a+")
        self.handler.logfile = self.logfile

    def set_handler(self, handler):
        """ unused provide a handlerclass for socketserver """
        self.handler = handler

    def set_cert(self, filename):
        """ providing a ssl certificate activates ssl-mode """
        self.cert_filename = filename

    def set_port(self, port):
        """ port server is listening to """
        self.port = port

    def start(self):
        """ startup, ssl-wrap and server_forever in a new thread """
        self.httpd = socketserver.ThreadingTCPServer(
            ("", self.port), self.handler, False
        )
        self.httpd.request_queue_size = 500
        self.httpd.timeout = 2000
        self.httpd.server_bind()
        self.httpd.server_activate()
        if self.cert_filename != "":
            self.httpd.socket = ssl.wrap_socket(
                self.httpd.socket, certfile=self.cert_filename, server_side=True
            )
        print("start serving")
        _thread.start_new_thread(self.httpd.serve_forever, ())

    def stop(self):
        """ cleanup in case of stopping the service """
        self.httpd.shutdown()
        self.logfile.close()
        print("server shutdown")
