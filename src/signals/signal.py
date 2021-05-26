import statistics

import numpy as np
from numpy.polynomial import Polynomial
from scipy.signal import find_peaks #pylint: disable=import-error

import signals.filter

from config import *

def intersect(f: np.ndarray,g: np.ndarray):
    idx = np.argwhere(np.diff(np.sign(f - g))).flatten()
    return idx


class Event(object):
    def __init__(self,start,end):
        self.start=start
        self.end=end
    
    def getdata(self,f: np.ndarray):
        out=f[self.start : self.end]
        return out
    
    def getpoly(self,f: np.ndarray):
        raise NotImplementedError
    

class Event_flatspot(Event):
    def __init__(self,start,end):
        Event.__init__(self,start,end)
    
    def getpoly(self,f: np.ndarray):
        x=np.arange(self.start,self.end)
        y=self.getdata(f)
        out=Polynomial.fit(x,y,1)
        return out
        
        

class Signal(object):
    def __init__(self,f):
        self.original=f
        self.data=f#np.array(f)
        self.calc()
    
    def filter(self,myfilter :signals.filter.Filter):
        myfilter.filter(self.data)
        self.calc()
    
    def deriv(self,n=1):
        return np.diff(self.data,n)
    
    def calc(self):
        #heartbeats
        peaks_pos=find_peaks(self.data,prominence=700)
        peaks_neg=find_peaks(self.data*-1,prominence=700)
        if True:####temp!!!!
            self.inverted=False
            #self.R_peaks=peaks_pos
        else:
            self.inverted=True
            #self.R_peaks=peaks_neg

        #self.events=self.generate_events()

    def generate_events(self):
        pass



    
