# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 22:25:32 2015

@author: n4p
"""
#from lib.Config import Config
from lib import aggregator
import hmac
import urllib.parse
import urllib.request as ur
import base64


GET = 0x01
PUT = 0x02
DEL = 0x04
POST = 0x08

REQOK = 0x0
REQINV = 0x1
SRCINV = 0x2


class RequestHandler():
    conf = None
    svctype = None

    def __init__(self,conf):
        self.conf = conf
        self.result = []
                
    
    def handle(self,fType,line,path):
        try:
            o = urllib.parse.urlparse(path)

            msg = o.path
            
            payload = urllib.parse.parse_qs(o.query,keep_blank_values=True)
            try:
                print(msg)
                response = REQINV
                groups = self.conf.valuelist('Blacklists/Groups/Group')
                for group in groups:
                    if msg[1:] == group.get('name'):
                        response = REQOK
                lists = self.conf.valuelist('Blacklists/Groups/Group[@name="'+msg[1:]+'"]/list')
                bl = []
                for item in lists:
                    bl.append({'name': item.get('name'), 'data': aggregator.normalize(ur.urlopen(item.get('url')))})
                self.result = aggregator.merge(bl)
                print(len(self.result))
                return response
            except:
                return SRCINV
        except:
            return REQINV
