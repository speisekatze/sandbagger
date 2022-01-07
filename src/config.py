# -*- coding: utf-8 -*-
"""
Config class reading xml config file
Created on Sun Mar 29 22:50:29 2015

@author: n4p
"""

import xml.etree.ElementTree as ET
import os.path
from os import environ


class Config:
    """ wrapper for reading config xml with xpath """

    root = None
    tree = None

    def __init__(self, filename="sandbagger.conf"):
        f = 'ext/' + filename
        if not os.path.isfile(f):
            f = 'config/' + filename
        print('loading ' + f)
        self.tree = ET.parse(f)
        self.root = self.tree.getroot()

    def value(self, xpath):
        """ return first found option matching xpath """
        # check ENV first
        var_name = xpath.split('/')[-1].upper()
        e = environ.get(var_name)
        if e is not None:
            return e
        return self.root.findall(xpath)[0].text

    def valuelist(self, xpath):
        """ return list of config options """
        return self.root.findall(xpath)
