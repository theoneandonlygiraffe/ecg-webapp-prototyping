import numpy as np

def intersect(f: np.ndarray,g: np.ndarray):
    idx = np.argwhere(np.diff(np.sign(f - g))).flatten()
    return idx

def getpoly(self,f: np.ndarray):# just to have acces to to polynomial for display
        x=np.arange(f.size)
        return Polynomial.fit(x,f,self.degr)