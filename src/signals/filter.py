from data.JSONinterface import JSONEncodable

from scipy.signal import savgol_filter #pylint: disable=import-error
import numpy as np
from numpy.polynomial import Polynomial

import statistics

class Filter(JSONEncodable):
    def filter(self,f: np.ndarray):
        raise NotImplementedError

class Filter_savgol(Filter):
    def __init__(self,windowlength,polyorder):
        self.windowlength=windowlength
        self.polyorder=polyorder
    def filter(self,f: np.ndarray):
        return savgol_filter(f,self.windowlength,self.polyorder)

class Filter_threshold(Filter):
    def __init__(self,threshold):
        self.threshold=threshold
    def filter(self,f: np.ndarray):
        out=[]
        for i in range(f.size-1):
            if abs(f[i]) < self.threshold:
                out.append(0)
            else:
                out.append(f[i])
        return np.array(out)

class Filter_threshold_binary(Filter):
    def __init__(self,threshold):
        self.threshold=threshold
    def filter(self,f: np.ndarray):
        out=[]
        for i in range(f.size-1):
            if abs(f[i]) < self.threshold:
                out.append(0)
            else:
                out.append(1)
        return np.array(out)

class Filter_polyfit(Filter):
    def __init__(self,degr=1):
        self.degr=degr

    def getpoly(self,f: np.ndarray):# just to have acces to to polynomial for display
        x=np.arange(f.size)
        return Polynomial.fit(x,f,self.degr)

    def filter(self,f: np.ndarray):
        x=np.arange(f.size)
        poly=self.getpoly(f)
        out=f-poly(x)
        return out
    
class Filter_complex_deriv(Filter):
    def __init__(self,threshold_deriv,amplifier,windowlength,polyorder):
        self.threshold_deriv=threshold_deriv
        self.amplifier=amplifier
        self.windowlength=windowlength
        self.polyorder=polyorder

    def filter(self,f: np.ndarray):
        thresholdfilter=Filter_threshold_binary(self.threshold_deriv)
        savgolfilter=Filter_savgol(self.windowlength,self.polyorder)

        deriv1=thresholdfilter.filter(savgolfilter.filter(f*self.amplifier))

        return deriv1

class Filter_complex_flatspot(Filter):
    def __init__(self,windowsize,filter_deriv1,filter_deriv2):
        self.filter_deriv1=filter_deriv1
        self.filter_deriv2=filter_deriv2
    def filter(self,f: np.ndarray):
        myfilter=self.filter_deriv1
        deriv1=myfilter.filter(np.diff(f,1))

        myfilter2=self.filter_deriv2
        deriv2=myfilter2.filter(np.diff(f,2))

        flatspotcurve=[]
        for i in range(deriv2.size):
            if deriv1[i]==0 and deriv2[i]==0:
                flatspotcurve.append(0)
            else:
                flatspotcurve.append(1)
            
        flatspotcurve=np.array(flatspotcurve)

        windowsize=20
        reach=int(windowsize/2)
        out=[]
        for i in range(reach):
            out.append(0)
        for i in range(0+reach,deriv2.size-reach-1):
            x=np.arange(i-reach,i+reach)
            avrg=statistics.mean(flatspotcurve[x])
            out.append(avrg)
        
        flatspotcurve=np.array(out)

        return flatspotcurve
