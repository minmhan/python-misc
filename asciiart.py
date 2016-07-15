# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 20:00:59 2016

@author: minmhan
"""

import sys, random, argparse
import numpy as np
import math
from PIL import Image

# 70 levels of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
# 10 levels of gray
gscale2 = "@%#*+=-:. "

def getAgerageL(image):
    # Given PIL Image, return average value of grayscale value 
    # get image as numpy array
    im = np.array(image)
    w,h = im.shape
    return np.average(im.reshape(w*h))


def convertImageToAscii(fileName, cols, scale, moreLevels):
    global gscale1, gscale2
    # open image and convert to grayscale
    image = Image.open(fileName).convert('L')
    W, H = image.size[0], image.size[1]
    print("imput image dims: %d x %d" % (W, H))
    # compute tile width
    w = W/cols
    # compute tile height based on aspect ratio and scale of the font
    h = w/scale
    # compute number of rows to use in final grid
    rows = int(H/h)
    
    print("cols: %d, rows: %d" % (cols, rows))
    print("tile dims: %d x %d" % (w, h))
    
    # check if image size is too small
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)
        
    aimg = []
    # generate the list of tile dimension
    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)
        #correct the last tile
        if j == rows-1:
            y2 = H
        
        aimg.append('')
        for i in range(cols):
            # crop image to fit the tile
            x1 = int(i*w)
            x2 = int((i+1)*w)
            if i == cols-1:
                x2 = W
                
            # crop the image to extrace the tile into another Image object
            img = image.crop((x1,y1,x2,y2))
            # get average luminance
            avg = int(getAgerageL(img))
            # look up ASCII char for grayscale value (avg)
            if moreLevels:
                gsval = gscale1[int((avg*69)/255)]
            else:
                gsval = gscale2[int((avg*9)/255)]
            aimg[j] += gsval
            
    return aimg
                
            

def main():
    # create parser
    descStr = 'This program converts an image into ASCII art.'
    parser = argparse.ArgumentParser(description=descStr)
    # add expected arguments
    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--out', dest='outFile', required=False)
    parser.add_argument('--cols', dest='cols', required=False)
    parser.add_argument('--morelevels', dest='moreLevels', action='store_true')
    
    # parse arguments
    args = parser.parse_args()
    imgFile = args.imgFile
    #set output file
    outFile = 'out.txt'
    if args.outFile:
        outFile = args.outFile
    # set scale default as 0.43, which suits a Courier font
    scale = 0.43
    if args.scale:
        scale = float(args.scale)
    # set cols
    cols = 80
    if args.cols:
        cols = int(args.cols)
    
    print('generating ASCII art...')
    aimg = convertImageToAscii(imgFile, cols, scale, args.moreLevels)
    
    # open a new text file
    f = open(outFile, 'w')    
    for row in aimg:
        f.write(row + '\n')
    f.close()
    print("ASCII art written to %s" % outFile)
    
    
if __name__ == '__main__':
    main()
    
    
    