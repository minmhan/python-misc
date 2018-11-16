# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 19:38:22 2018

@author: minmh
python arxiv_downloader.py -s3 C:\Projects\Python\s3cmd\s3cmd -f arXiv_pdf_manifest.xml -o D:\arXiv\pdf
"""

import sys
from argparse import ArgumentParser
import subprocess
import xml.etree.ElementTree as et
import logging
import time

logging.basicConfig(filename='arxiv_downloader.log', filemode='w')

def main(**args):
    manifestfile = args['manifestfile']
    #mode = args['mode']
    outdir = args['outputdir']
    s3cmd = args['s3cmd']
    print(s3cmd)
    
    tree = et.parse(manifestfile)
    filenames = tree.findall('./file/filename')
    for f in filenames:
        download(s3cmd, f.text, outdir)

def download(s3cmd, file, outdir):
    cmd = 'python {} get --requester-pays s3://arxiv/{} {}'.format(s3cmd, file, outdir)
    print(cmd)
    try:
        proc = subprocess.Popen(cmd)
        while proc.poll() is None:
            time.sleep(0.1)
            
        logging.debug(file)
    except KeyboardInterrupt:
        proc.terminate()
        raise
    except:
        logging.error("Error:" + file)
    
if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument('--s3cmd','-s3', type=str, help='s3cmd tool')
    ap.add_argument('--manifestfile', '-f', type=str, help='Manifest file')
    ap.add_argument('--outputdir', '-o', type=str, help='Output directory')
    #ap.add_argument('--mode','-m',type=str, choices=set(('pdf','src')), help='Pdf or Src')
    
    args = ap.parse_args()
    main(**vars(args))