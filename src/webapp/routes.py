from webapp import app

import matplotlib.pyplot as plt #pylint: disable=import-error
import numpy as np
import mpld3 #pylint: disable=import-error
import ingest
import signals
import statistics

from config import *


@app.route('/')
@app.route('/index')
def index():
    fig, ax = plt.subplots(figsize=(6, 2), dpi=265)
    
    y=ingest.ptbdiagnostic.curve_from_file_ptb("../data/raw/ptb-diagnostic-ecg-database-1.0.0/patient041/s0138lre.dat",12,1)[:2000]

    polyfilter=global_polyfilter_signal
    savgolfilter=global_savgolfilter_signal

    y=savgolfilter.filter(y)

    newy=polyfilter.filter(y)
    x=np.arange(y.size)

    #ax.margins(0.05)
    fig.tight_layout(pad=0.03)   
    #original curve 
    #ax.plot(x,y,color="grey")
    #ax.plot(x,np.zeros(x.size),"--",color="grey")
    #polynomial
    #ax.plot(x,polyfilter.getpoly(y)(x),color="green")
    #newcurve
    ax.plot(x,newy,color="grey")
    
    lead1=signals.signal.Signal(newy)
    #ax.plot(lead1.events,newy[lead1.events],"X",color="black")



    #eventcurve
    myfilter=global_complexfilter_eventcurve_deriv1
    deriv1=myfilter.filter(lead1.deriv(1))
    ax.plot(np.arange(deriv1.size),deriv1*200+500,"--",color="green")

    myfilter2=global_complexfilter_eventcurve_deriv2
    deriv2=myfilter2.filter(lead1.deriv(2))
    ax.plot(np.arange(deriv2.size),deriv2*200+200,"--",color="blue")

    flatspotfilter=global_complexfilter_eventcurve_flats
    curve_flatspots=flatspotfilter.filter(lead1.data)
    ax.plot(np.arange(curve_flatspots.size),curve_flatspots*200-300,"-",color="red")

    zero=np.zeros(curve_flatspots.size)
    idx=signals.signal.intersect(curve_flatspots,zero)
    




    #ax.grid(color='white', linestyle='solid')
    #ax.set_title("Scatter Plot (with tooltips!)", size=20)

    string=mpld3.fig_to_html(fig)
    return string