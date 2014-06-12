# -*- coding: utf-8 -*-
"""
A collection of widgets for gui building

Copyright: Jev Kuznetsov
License: BSD
"""

from __future__ import division

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class MatplotlibWidget(QWidget):
    def __init__(self,parent=None,grid=True):
        QWidget.__init__(self,parent)
        
        self.grid = grid        
        
        
        self.fig = Figure()
        self.canvas =FigureCanvas(self.fig)
        self.canvas.setParent(self)      
        self.canvas.mpl_connect('button_press_event', self.onPick) # bind pick event  
        
        
        #self.axes = self.fig.add_subplot(111)
        margins = [0.05,0.1,0.9,0.8]
        self.axes = self.fig.add_axes(margins)
        self.toolbar = NavigationToolbar(self.canvas,self)
        
              
        #self.initFigure()
        
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)        
        
        self.setLayout(layout)        
    
    def onPick(self,event):
        print 'Pick event'
        print 'you pressed', event.button, event.xdata, event.ydata
    
    def update(self):
        self.canvas.draw()
        
    def plot(self,*args,**kwargs):
        self.axes.plot(*args,**kwargs)
        self.axes.grid(self.grid)
        self.update()

    def clear(self):
        self.axes.clear()
    
    def initFigure(self):
        self.axes.grid(True)   
        x = np.linspace(-1,1)
        y = x**2
        self.axes.plot(x,y,'o-')


class PlotWindow(QMainWindow):
    ''' a stand-alone window with embedded matplotlib widget '''
    def __init__(self,parent=None):
        super(PlotWindow,self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.mplWidget = MatplotlibWidget()
        self.setCentralWidget(self.mplWidget)
    
    def plot(self,dataFrame):
        ''' plot dataframe '''
        dataFrame.plot(ax=self.mplWidget.axes)
    
    def getAxes(self):
        return self.mplWidget.axes
    
    def getFigure(self):
        return self.mplWidget.fig

    def update(self):
        self.mplWidget.update()

class MainForm(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Demo: PyQt with matplotlib')
        
        self.plot = MatplotlibWidget()
        self.setCentralWidget(self.plot)
        
        self.plot.clear()
        self.plot.plot(np.random.rand(10),'x-')
        
        
#---------------------
if __name__=='__main__':
    app = QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()