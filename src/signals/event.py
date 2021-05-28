import numpy as np
from numpy.polynomial import Polynomial

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