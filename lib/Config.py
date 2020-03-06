# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 22:50:29 2015

@author: n4p
"""

import xml.etree.ElementTree as ET


class Config():
    root = None
    tree = None

    def __init__(self, filename):
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()
        
    def value(self,xpath):
        return self.root.findall(xpath)[0].text

    def valuelist(self,xpath):
        return self.root.findall(xpath)  

         