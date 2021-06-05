import numpy as np

from scipy.fft import rfft, rfftfreq

from scipy import signal
from scipy.signal import find_peaks #pylint: disable=import-error

def fft(f :np.ndarray,SAMPLE_RATE,frequencies=(0,500)):
    N=f.size

    yf = rfft(f)
    yf = np.abs(yf)

    xf = rfftfreq(N, 1 / SAMPLE_RATE)
    #freq range
    trimmed_xf=[]
    trimmed_yf=[]
    for i in range(xf.size):
        freq=xf[i]
        if freq >=frequencies[0] and freq <=frequencies[1]:
            trimmed_xf.append(xf[i])
            trimmed_yf.append(yf[i])
    
    xf=np.array(trimmed_xf)
    yf=np.array(trimmed_yf)
    
    return xf,yf


def freq_peaks(f :np.ndarray,SAMPLE_RATE,num_peaks=10,freq_trim=(0,500),plt=None):
    xf,yf=fft(f,SAMPLE_RATE,frequencies=freq_trim)

    peaks_idx_in_yf=find_peaks(yf,prominence=2000)[0]#try without prominence

    peaks_frequency_value=xf[peaks_idx_in_yf]

    peaks_idx=peaks_idx_in_yf[np.argsort(yf[peaks_idx_in_yf])[-num_peaks:]]
    peaks=xf[peaks_idx]


    #display to mlp
    if plt:
        #fft
        plt.plot(xf,yf**2,"-",color="blue")
        #all peaks
        #plot.plot(peaks_frequency_value,yf[peaks_idx_in_yf],"x",color="green")
        #returned peaks
        plt.plot(peaks,yf[peaks_idx]**2,"x",color="red")
        
    return peaks

def band_stop(f :np.ndarray,SAMPLE_RATE,target_freq,Q=10):

    # Design notch filter
    b, a = signal.iirnotch(target_freq, Q, SAMPLE_RATE)

    zi = signal.lfilter_zi(b, a)
    z, _ = signal.lfilter(b, a, f, zi=zi*f[0])

    z2, _ = signal.lfilter(b, a, z, zi=zi*z[0])


    out = signal.filtfilt(b, a, f)
    return out

def band_pass(f: np.ndarray,SAMPLE_RATE, freq_trim=(1,20), order=5):
    nyq = 0.5 * (SAMPLE_RATE)
    low = freq_trim[0] / nyq
    high = freq_trim[1] / nyq

    b, a = signal.butter(order, [low, high], btype='band')

    y = signal.lfilter(b, a, f)
    return y