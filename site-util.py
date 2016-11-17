# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 20:25:10 2016

@author: minmhan
"""

import argparse
from urllib import request
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def crawl(pages, depth=5):
    totalpages=[]
    domain = getdomain(pages[0])
    for i in range(depth):
        newpages=set()
        for page in pages:
            # TODO: subdomain
            if getdomain(page) != domain:
                continue
            
            try:
                c=request.urlopen(page)
            except:
                print('could not open %s' % page)
                continue
            soup = BeautifulSoup(c.read(), 'html.parser')
            totalpages.append(page)
            print("indexing :", page)
            links=soup('a')
            #print(soup)
            for link in links:
                if('href' in dict(link.attrs)):
                    url= urljoin(page,link['href'])
                    if url.find("'")!=-1: continue
                    url=url.split('#')[0] #remove location portion
                    if url[0:4]=='http' and not url in totalpages:
                        newpages.add(url)
                        
                        
        pages = newpages
    print("Total pages: %d" % len(totalpages))


def getdomain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return domain

def main():
    # create parser
    descStr = 'This program count approximate pages in a website.'
    parser = argparse.ArgumentParser(description=descStr)
    # add expected arguments
    parser.add_argument('--url', dest='url', required=True)
    
    # parse arguments
    args = parser.parse_args()
    url = args.url
    crawl([url])
    
crawl(['http://www.mizzima.com/'])