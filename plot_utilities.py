# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 06:06:53 2020

@author: kenzo
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
import matplotlib
#matplotlib.rc('xtick', labelsize=10)     
#matplotlib.rc('ytick', labelsize=10)

        
        
class plot_utilities:
    
    def __init__(self, nrows = 1, ncols = 1,xaxis = None, yaxis = None, lw = 2, xlabel = None, ylabel = None, costume_fontsize = 12, color = 'r', ls = '-', marker = None, label = None):
        self.font = {
        #'family': 'serif', 'serif': ['Computer Modern'],
        'family': 'sans-serif',
        'sans-serif':'Helvetica',
        'weight' : 'normal',
        'size'   : 20}
        self.axes = {
        'titlesize'  : 20,
        'labelsize'  : 20,
        'labelweight': 'normal'
                }
        self.xtick = {
        'labelsize' :  30
                }
        self.ytick = {
        'labelsize' :  30
                }
        matplotlib.rc('text.latex', preamble=[r'\usepackage{amsmath}',r'\usepackage{physics}',r'\usepackage[helvet]{sfmath}'])
        matplotlib.rc('font', **self.font)
        matplotlib.rc('text', usetex = True)
        matplotlib.rc('axes', **self.axes)
        matplotlib.rc('xtick', **self.xtick)
        matplotlib.rc('ytick', **self.ytick)
        matplotlib.rc('figure', figsize = (10,8))
        self.xdata = np.linspace(0,100,150)
        self.ydata = np.sin(self.xdata)
        self.xaxis = xaxis
        self.yaxis = yaxis
        self.lw = lw
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.color = color
        if marker != None:
            self.ls = ""
        else:
            self.ls = ls
        self.custome_fontsize = costume_fontsize
        self.marker = marker
        self.fig, self.ax = plt.subplots(nrows, ncols)
        self.label = label
        self.fillstyle = 'full'

        
    
    
    def plot(self, xdata = None, ydata = None, label = None, ax = None, markersize = 12):
        if (xdata == None).all():
            xdata = self.xdata
            ydata = self.ydata
        if label == None:
            label = self.label
        if ax == None:
            ax = self.ax
        ax.plot(xdata, ydata, color = self.color, lw = self.lw, ls = self.ls, marker = self.marker, label = label, markersize = markersize, fillstyle = self.fillstyle)
        ax.set_xlabel(self.xlabel, fontsize = 30)
        ax.set_ylabel(self.ylabel, fontsize = 30)
    
    def error_bar(self, xdata = None, ydata = None, xerr = 0, yerr = 0, label = None, ax = None, markersize = 12, uplims = False, lolims = False, capsize = 0):
        if (xdata == None).all():
            xdata = self.xdata
            ydata = self.ydata
        if label == None:
            label = self.label
        if ax == None:
            ax = self.ax
        ax.errorbar(xdata, ydata, xerr = xerr, yerr = yerr, color = self.color, lw = self.lw, ls = self.ls, marker = self.marker, label = label, markersize = markersize, fillstyle = self.fillstyle, uplims = uplims, lolims = lolims, capsize = capsize)
        ax.set_xlabel(self.xlabel, fontsize = 30)
        ax.set_ylabel(self.ylabel, fontsize = 30)
        
    def inset(self, xdata, ydata, xlim, ylim, zoom = 10, loc = "center", xticks = 7, yticks = 7, label = None):
        axins = zoomed_inset_axes(self.ax, zoom = zoom, loc = loc)
        #axins.plot(xdata, ydata,  color = self.color, lw = self.lw, ls = self.ls, marker = self.marker, label = self.label)
        axins.set_xlim(xlim[0],xlim[1])
        axins.set_ylim(ylim[0],ylim[1])
        mark_inset(self.ax, axins, loc1=1, loc2=2, fc="none", ec='0.5')
        axins.yaxis.get_major_locator().set_params(nbins=yticks)
        axins.xaxis.get_major_locator().set_params(nbins=xticks)
        return axins
    
    def set_font(self):
        matplotlib.rc('font', **self.font)
    def set_axes(self):
        matplotlib.rc('axes', **self.axes)
    def set_ticks(self):
        matplotlib.rc('xtick', **self.xtick)
        matplotlib.rc('ytick', **self.ytick)
    def set_size(self, x, y):
        matplotlib.rc('figure', figsize = (x,y))
    def set_layout(self):
        plt.tight_layout()
        
        
        
        