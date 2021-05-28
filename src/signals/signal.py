import statistics

import numpy as np
from numpy.polynomial import Polynomial
from scipy.signal import find_peaks #pylint: disable=import-error

import signals.filter

from config import *


 

class Signal(object):
    def __init__(self,f):
        self.original=f
        self.data=f#np.array(f)
        self.recalc()
    
    def filter(self,myfilter :signals.filter.Filter):
        myfilter.filter(self.data)
        self.calc()
    
    def deriv(self,n=1):
        return np.diff(self.data,n)
    
    def recalc(self):

        #flatspotdetection
        myfilter=global_complexfilter_eventcurve_deriv1
        deriv1=myfilter.filter(self.deriv(1))

        myfilter2=global_complexfilter_eventcurve_deriv2
        deriv2=myfilter2.filter(self.deriv(2))
        
        flatspotfilter=global_complexfilter_eventcurve_flats
        self.curve_flatspots=flatspotfilter.filter(self.data)
    


        #peaks
        peaks_pos=find_peaks(self.data,prominence=120)[0]
        peaks_neg=find_peaks(self.data*-1,prominence=120)[0]

        peaks=np.concatenate((peaks_pos,peaks_neg))
        out=[]
        for peak in peaks:
            if self.curve_flatspots[peak]==0:
                pass
            else:
                out.append(peak)
        self.peaks=out








class ECG_Lead(Signal):
    def __init__(self,f):
        Signal.__init__(self,f)

    def recalc(self):
        Signal.recalc(self)
        #heartbeats
        peaks_pos=find_peaks(self.data,prominence=700)[0]
        peaks_pos_avrg=abs(self.data[peaks_pos].mean())
        peaks_neg=find_peaks(self.data*-1,prominence=700)[0]
        peaks_neg_avrg=abs(self.data[peaks_neg].mean())


        if peaks_pos_avrg>=peaks_neg_avrg:
            self.inverted=False
            self.R_peaks=peaks_pos
        else:
            self.inverted=True
            self.R_peaks=peaks_neg


