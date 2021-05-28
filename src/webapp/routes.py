from signals import utility
from webapp import app
import flask


import matplotlib.pyplot as plt #pylint: disable=import-error
import numpy as np
import mpld3 #pylint: disable=import-error
import ingest
import signals
import statistics

from config import *

from numpy.polynomial import Polynomial

from scipy.fft import rfft, rfftfreq

from scipy import signal
from scipy.signal import find_peaks #pylint: disable=import-error


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

    buttonstring_next='<button onclick="window.location.href='+"'/ecg_view?sample_index="+str(sample_index+1)+"&signal_index="+str(signal_index)+"&filter=auto"+"'"+';"> > </button>'
    buttonstring_prev='<button onclick="window.location.href='+"'/ecg_view?sample_index="+str(sample_index-1)+"&signal_index="+str(signal_index)+"&filter=auto"+"'"+';"> < </button>'

    buttonstring_up='<button onclick="window.location.href='+"'/ecg_view?sample_index="+str(sample_index)+"&signal_index="+str(signal_index-1)+"&filter=auto"+"'"+';"> - </button>'
    buttonstring_down='<button onclick="window.location.href='+"'/ecg_view?sample_index="+str(sample_index)+"&signal_index="+str(signal_index+1)+"&filter=auto"+"'"+';"> + </button>'
    
    
    
    
    string =string+buttonstring_prev+buttonstring_next+buttonstring_up+buttonstring_down
    
    
    







    fig, axs = plt.subplots(2,1,figsize=(6, 3), dpi=265)

    ax=axs[0]
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
    
    lead1=signals.signal.ECG_Lead(newy)
    #ax.plot(lead1.events,newy[lead1.events],"X",color="black")
    ax.plot(lead1.R_peaks,lead1.data[lead1.R_peaks],"x",color="red")



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

    # Number of sample points
    SAMPLE_RATE = 1000
    N=7000


    yf = rfft(lead1.data)[:500]**2
    xf = rfftfreq(N, 1 / SAMPLE_RATE)[:500]
    yf=np.abs(yf)
    peaks_realx=find_peaks(yf,prominence=2000)[0]

    peaks_frequency=xf[peaks_realx]#xf[] is important so frequency matches // shift between freq and "realworld" x
    
    plot_fft=axs[1]


    plot_fft.plot(peaks_frequency,yf[peaks_realx],"x",color="red")#xf[] is important so frequency matches
    plot_fft.plot(xf,yf,"-",color="blue")
    
    peaks_idx=peaks_realx[np.argsort(yf[peaks_realx])[:-1]]
    peaks=xf[peaks_idx]
    
    plot_fft.plot(peaks,yf[peaks_idx],"x",color="green")

    

    #frq filter
    orig=lead1.data
    filter_freq=flask.request.args.get('filter')

    if filter_freq:
        if filter_freq=="auto":
            freqs=peaks
        else:
            freqs=filter_freq.split()

        for freq in freqs:
            freq=float(freq)


            fs = 1000.0  # Sample frequency (Hz)
            f0 = freq  # Frequency to be removed from signal (Hz)
            Q = 10.0  # Quality factor
            # Design notch filter
            b, a = signal.iirnotch(f0, Q, fs)

            zi = signal.lfilter_zi(b, a)
            z, _ = signal.lfilter(b, a, orig, zi=zi*orig[0])

            z2, _ = signal.lfilter(b, a, z, zi=zi*z[0])

            out = signal.filtfilt(b, a, orig)
            orig=out

        ax.plot(np.arange(out.size),out,"--",color="green")
    
    string=string+mpld3.fig_to_html(fig)
    string+="dominant freq:"+str(xf[peaks_idx[-1]])+"\n"
    string += "freq peaks:"+str(peaks)
    return string