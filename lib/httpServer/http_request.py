# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:19:44 2015

@author: n4p
"""

import http.server
import datetime
import urllib.parse
import urllib.request as ur
from lib import aggregator
from lib import config

__version__ = "0.2"

REQOK = 0x0
REQINV = 0x1
SRCINV = 0x2
UNKNOWN = 0x4


def get_help_text():
    """ compile some kind of error page """
    help_html = "<html><head><title>Error</title></head><body>"
    help_html += "<h1>Avaiable Blocklist Groups</h1>"
    help_html += "<p>Just append the name of the blocklist to the path like"
    help_html += " http(s)://blocklist.somewhere.org/social</p><ul>"
    groups = config.Config().valuelist("Blacklists/Groups/Group")
    for group in groups:
        help_html += "<li>" + group.get("name") + "</li>"
    help_html += "</ul></body>"
    return help_html


class HttpRequest(http.server.BaseHTTPRequestHandler):
    """ simple class to handle our HTTP requests """

    server_version = "httpd/sandbagger " + __version__
    response = []
    logfile = None
    result = []

    def do_GET(self):
        """Serve a GET request."""
        self.send_head()

    def do_HEAD(self):
        """Serve a HEAD request."""
        self.send_head()

    def send_head(self):
        """ currently handles all different requests """
        handler_result = None
        path = urllib.parse.unquote(self.path)
        handler_result = self.process_request(path)
        if handler_result == REQOK:
            self.send_response(200)
            self.send_header("Content-type", "text/text; charset=%s" % "UTF-8")
            date = self.date_time_string(
                datetime.datetime.timestamp(datetime.datetime.now())
            )
            self.send_header("Last-Modified", date)
            out = ""
            if len(self.result) > 0:
                for line in self.result:
                    out += line + "\r\n"
                self.send_header("Content-Length", str(len(out)))
                self.end_headers()
                self.log_message("served %d urls" % len(self.result))
                self.wfile.write(out.encode("utf8"))
        else:
            if handler_result == REQINV:
                self.send_response(404)
                self.log_message("path not found - path: %s" % path)
            elif handler_result == SRCINV:
                self.send_response(501)
                self.log_message("something went wrong - path: %s" % path)
            else:
                self.send_response(500)
                self.log_message("something went wrong - path: %s" % path)
            help_string = get_help_text()
            self.send_header("Content-type", "text/html; charset=%s" % "UTF-8")
            self.send_header("Content-Length", str(len(help_string)))
            self.end_headers()
            self.wfile.write(help_string.encode("utf8"))

    def process_request(self, path):
        """ Process requests - get blocklist urls from config
            for category name given by request and call aggregator """
        try:
            get_request = urllib.parse.urlparse(path)
            msg = get_request.path
            conf = config.Config()
            try:
                response = REQINV
                groups = conf.valuelist("Blacklists/Groups/Group")
                for group in groups:
                    group_name = group.get("name")
                    if msg[1:] == group_name:
                        response = REQOK
                        lists = conf.valuelist(
                            'Blacklists/Groups/Group[@name="' + group_name + '"]/list'
                        )
                        blocklist = []
                        for item in lists:
                            blocklist_data = aggregator.normalize(
                                ur.urlopen(item.get("url"))
                            )
                            blocklist.append(
                                {"name": item.get("name"), "data": blocklist_data}
                            )
                        self.result = aggregator.merge(blocklist)
                return response
            except Exception as error:
                self.log_message("Error '{0}' occured." % (error))
                return SRCINV
        except Exception as error:
            self.log_message("Error '{0}' occured." % (error))
            return REQINV
        else:
            self.log_message("should not get here")
            return UNKNOWN

    def log_message(self, format, *args):
        """ writes message to log """
        address = self.address_string()
        date_time = self.log_date_time_string()
        self.logfile.write("%s - - [%s] %s\n" % (address, date_time, format % args))
