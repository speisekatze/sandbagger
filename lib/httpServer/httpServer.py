# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 14:22:28 2015

@author: n4p
"""
__version__ = "0.01"
import http.server
import socketserver
import _thread
import ssl
#import httpRequest

class httpServer():
    Handler = None
    httpd = None
    Port = 0
    CertfileName = ''
    LogFile = None              
        
    def __init__(self,handler = None,port = None):
        self.Handler = handler
        self.Port = port      
        self.LogFile = open("httpd.log", "a+")
        self.Handler.LogFile = self.LogFile
        
    def setHandler(self,h):
        self.Handler = h
        
    def setCert(self,filename):
        self.CertfileName = filename
        
    def setPort(self,p):
        self.Port = p
        
    def start(self):
        self.httpd = socketserver.ThreadingTCPServer(("", self.Port), self.Handler, False)
        self.httpd.request_queue_size = 500
        self.httpd.timeout = 2000
        self.httpd.server_bind()
        self.httpd.server_activate()
        if self.CertfileName != '':
            self.httpd.socket = ssl.wrap_socket (self.httpd.socket, certfile=self.CertfileName, server_side=True)
        print('start serving')
        _thread.start_new_thread( self.httpd.serve_forever, () )
        
    def stop(self):
        self.httpd.shutdown()
        self.LogFile.close()
        print('server shutdown')
    
