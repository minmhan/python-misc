# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 21:10:15 2016

@author: minmhan
"""

import matplotlib.pylab as plt
import numpy as np
import time

fig = plt.figure()
ax = fig.add_subplot(111)

x = np.arange(10000)
y = np.random.randn(10000)

li, = ax.plot(x,y)

#draw and show
fig.canvas.draw()
plt.ion()
plt.show(block=False)

while True:
    try:
        y[:-10] = y[10:]
        y[-10:] = np.random.randn(10)
        
        #set new data
        li.set_ydata(y)
        fig.canvas.draw()
        
        time.sleep(0.01)
        print('ploting')
    except KeyboardInterrupt:
        break