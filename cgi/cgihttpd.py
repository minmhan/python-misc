# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 11:52:02 2016

@author: minmhan
"""

from http.server import CGIHTTPRequestHandler, HTTPServer

PORT = 8080

httpd = HTTPServer(("", PORT), CGIHTTPRequestHandler)
print("serving at port", PORT)
httpd.serve_forever()