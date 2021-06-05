from signalprocessing import frequencies
from signals import utility
from webapp import app
import flask

import ingest
import signals
import signalprocessing


import matplotlib.pyplot as plt #pylint: disable=import-error
import numpy as np
import mpld3 #pylint: disable=import-error


from config import *

from numpy.polynomial import Polynomial

from scipy.fft import rfft, rfftfreq

from scipy import signal
from scipy.signal import find_peaks
import webapp #pylint: disable=import-error


@app.route('/')
@app.route('/ecg_view')
def show_ecg():


    string=""
    files=ingest.ptbdiagnostic.find_files_type(".dat","../data")

    sample_index=flask.request.args.get('sample_index')
    if not sample_index:
        sample_index=1
    else:
        sample_index=int(sample_index)
    
    sample_index=sample_index%len(files)
    
    signal_index=flask.request.args.get('signal_index')
    if not signal_index:
        signal_index=0
    else:
        signal_index=int(signal_index)

    signal_index=signal_index%12
    
    
    
    y=ingest.ptbdiagnostic.curve_from_file_ptb(files[sample_index],12,signal_index-1)[:7000]

    string += files[sample_index]

    buttonstring_next='<button onclick="window.location.href='+"'/ecg_view?sample_index="+str(sample_index+1)+"&signal_index="+str(signal_index)+""+"'"+';"> > </button>'
    buttonstring_prev='<button onclick="window.location.href='+"'/ecg_view?sample_index="+str(sample_index-1)+"&signal_index="+str(signal_index)+""+"'"+';"> < </button>'

    buttonstring_up='<button onclick="window.location.href='+"'/ecg_view?sample_index="+str(sample_index)+"&signal_index="+str(signal_index-1)+""+"'"+';"> - </button>'
    buttonstring_down='<button onclick="window.location.href='+"'/ecg_view?sample_index="+str(sample_index)+"&signal_index="+str(signal_index+1)+""+"'"+';"> + </button>'
    
    
    
    
    string =string+buttonstring_prev+buttonstring_next+buttonstring_up+buttonstring_down
    
    
    







    fig, axs = plt.subplots(2,1,figsize=(6, 3), dpi=265)

    ax=axs[0]
    polyfilter=global_polyfilter_signal
    savgolfilter=global_savgolfilter_signal

    y=savgolfilter.filter(y)
    #y=signalprocessing.frequencies.band_pass(y,1000.0,freq_trim=(0.01,50),order=3)


    newy=polyfilter.filter(y)
    x=np.arange(y.size)

    #ax.margins(0.05)
    fig.tight_layout(pad=0.03)   

    #newcurve
    ax.plot(x,newy,color="grey")
    
    lead1=signals.signal.ECG_Lead(newy)

    #plot beats
    ax.plot(lead1.R_peaks,lead1.data[lead1.R_peaks],"x",color="red")


    #plot peaks
    ax.plot(lead1.peaks,lead1.data[lead1.peaks],"x",color="black")
    #ax.plot(lead1.peaks_neg,lead1.data[lead1.peaks_neg],"X",color="black")


    #eventcurve
    flatspotfilter=global_complexfilter_eventcurve_flats
    curve_flatspots=flatspotfilter.filter(lead1.data)
    #ax.plot(np.arange(curve_flatspots.size),curve_flatspots*200-300,"-",color="red")

    #events
    zero=np.zeros(curve_flatspots.size)
    idx=signals.utility.intersect(curve_flatspots,zero)

    for i in range(len(idx)-1):
        if lead1.curve_flatspots[idx[i]+1]==0:
            if abs(idx[i]-idx[i+1])>20:
                x=np.arange(idx[i],idx[i+1])
                poly=Polynomial.fit(x,lead1.data[x],1)
                ax.plot(x,poly(x),color="red")
    




    #ax.grid(color='white', linestyle='solid')
    #ax.set_title("Scatter Plot (with tooltips!)", size=20)



    #fourier transform
    peaks=signalprocessing.frequencies.freq_peaks(lead1.data,1000,freq_trim=(0,100),plt=axs[1])

    

    #band stop filter
    orig=lead1.data
    filter_freq=flask.request.args.get('filter')

    if filter_freq:
        low=float(filter_freq)-0.1
        high=float(filter_freq)+0.1

        orig=signalprocessing.frequencies.band_pass(orig,1000.0,freq_trim=(low,high),order=1)

        ax.plot(np.arange(orig.size),orig,"--",color="green")
    
    string=string+mpld3.fig_to_html(fig)
    #string+="dominant freq:"+str(xf[peaks_idx[-1]])+"\n"
    string += "freq peaks:"+str(peaks)
    return string

@app.route('/freq_single_lead')
def show_freq_single_lead():

    http_body,y=webapp.requests.wrap_temp_sample_switch("/freq_single_lead")

    y=global_savgolfilter_signal.filter(y)
    y=global_polyfilter_signal.filter(y)
    x=np.arange(y.size)

    #freqs
    num_peaks=webapp.requests.int_request_argument('num_peaks',5)
    #no protection
    
    #,figsize=(6, (2+num_peaks))
    fig, axs = plt.subplots(2+num_peaks,1, dpi=265)

    axs[1].plot(x,y,color="black")
    peaks=signalprocessing.frequencies.freq_peaks(y,1000,freq_trim=(0,2),plt=axs[0],num_peaks=num_peaks)

    for i in range(peaks.size):
        plot=axs[peaks.size-i+1]

        window_width=0.4

        low=peaks[i]-window_width/2
        high=peaks[i]+window_width/2

        while 0>low:
            low+=0.01
            high-=0.01

        

        out=signalprocessing.frequencies.band_pass(y,1000.0,freq_trim=(low,high),order=1)

        plot.set_title("Freq: "+str(peaks[i]), size=20)
        #plot.grid("--",color='red')
        g=0.2
        b=0.2
        r=1/peaks.size*(peaks.size-i)
        plot.plot(np.arange(out.size),out,"-",color=(r,g,b,1.0))
        





    http_body+=mpld3.fig_to_html(fig)
    return http_body
