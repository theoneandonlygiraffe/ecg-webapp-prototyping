import signals.filter as filt

global_polyfilter_signal=filt.Filter_polyfit(1)
global_savgolfilter_signal=filt.Filter_savgol(101,8)


global_complexfilter_eventcurve_deriv1=filt.Filter_complex_deriv(90,50,101,5)
global_complexfilter_eventcurve_deriv2=filt.Filter_complex_deriv(50,200,151,7)
global_complexfilter_eventcurve_flats=filt.Filter_complex_flatspot(10,global_complexfilter_eventcurve_deriv1,global_complexfilter_eventcurve_deriv2)