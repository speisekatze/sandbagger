# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:19:44 2015

@author: n4p
"""

import http.server
import io
import json
import datetime
import shutil
import _thread
from lib import RequestHandler

__version__ = "0.01"

class httpRequest(http.server.BaseHTTPRequestHandler):

    server_version = "myHTTPd/" + __version__
    r = []
    LogFile = None
    externHandler = None
    
    def do_GET(self):
        """Serve a GET request."""
        self.r.append(['TYPE','GET'])
        f = self.send_head(RequestHandler.GET)
        if f:
            f.close()

    def do_HEAD(self):
        """Serve a HEAD request."""
        self.r.append(['TYPE','HEAD'])
        f = self.send_head()
        if f:
            f.close()

    def do_POST(self):
        self.r.append(['TYPE','POST'])
        f = self.send_head(RequestHandler.POST)
        if f:
            f.close()
            
    def do_PUT(self):
        self.r.append(['TYPE','PUT'])
        f = self.send_head(RequestHandler.PUT)
        if f:
            f.close()
            
    def do_DEL(self):
        self.r.append(['TYPE','DEL'])
        f = self.send_head(RequestHandler.DEL)
        if f:
            f.close()
    
    
    def send_head(self,fType):
        try:
            extHndlResult = None
            if (self.externHandler != None):
                extHndlResult = self.externHandler.handle(fType,self.raw_requestline,self.path)
            if (extHndlResult == RequestHandler.REQOK):
                self.r.append(['CMD','OK'])
                self.r.append(['RESP',None])
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=%s" % 'UTF-8')
                self.send_header("Last-Modified", self.date_time_string(datetime.datetime.timestamp(datetime.datetime.now())))
                out = ''
                if len(self.externHandler.result) > 0:
                    for line in self.externHandler.result:
                        out += line + "\r\n"
                    self.send_header("Content-Length", str(len(out)))
                    self.end_headers()
                    self.log_message('served %d urls' % len(self.externHandler.result))
                    self.wfile.write(out.encode("utf8"))
                    self.r.clear()
                    return 
            elif (extHndlResult == RequestHandler.REQINV):
                self.send_response(404)
                self.r.append(['CMD','NOK'])
                self.r.append(['RESP','InvalidRequest'])
                self.log_message('invalid request')
            elif (extHndlResult == RequestHandler.SRCINV):
                self.send_response(403)
                self.r.append(['CMD','NOK'])
                self.r.append(['RESP','InvalidSource'])
                self.log_message('invalid source')
            a = json.dumps(self.r).encode()
            self.send_header("Content-Length", str(len(a)))
            self.end_headers()
            f = io.BytesIO()
            f.write(a)
            f.seek(0)
            self.r.clear()
            self.copyfile(f, self.wfile)
            return f
            
        except:
            f.close()
            raise

    def copyfile(self, source, outputfile):
        shutil.copyfileobj(source, outputfile)
        
    def log_message(self, format, *args):
        self.LogFile.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format%args))


