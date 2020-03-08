# -*- coding: utf-8 -*-
"""
Config class reading xml config file
Created on Sun Mar 29 22:50:29 2015

@author: n4p
"""

import xml.etree.ElementTree as ET


class Config:
    """ wrapper for reading config xml with xpath """

    root = None
    tree = None

    def __init__(self, filename="Config/sandbagger.conf"):
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()

    def value(self, xpath):
        """ return first found option matching xpath """
        return self.root.findall(xpath)[0].text

    def valuelist(self, xpath):
        """ return list of config options """
        return self.root.findall(xpath)
