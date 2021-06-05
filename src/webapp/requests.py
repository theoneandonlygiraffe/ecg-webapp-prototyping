import ingest
import flask

def wrap_temp_sample_switch(view):
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

    buttonstring_next='<button onclick="window.location.href='+"'"+view+"?sample_index="+str(sample_index+1)+"&signal_index="+str(signal_index)+""+"'"+';"> > </button>'
    buttonstring_prev='<button onclick="window.location.href='+"'"+view+"?sample_index="+str(sample_index-1)+"&signal_index="+str(signal_index)+""+"'"+';"> < </button>'

    buttonstring_up='<button onclick="window.location.href='+"'"+view+"?sample_index="+str(sample_index)+"&signal_index="+str(signal_index-1)+""+"'"+';"> - </button>'
    buttonstring_down='<button onclick="window.location.href='+"'"+view+"?sample_index="+str(sample_index)+"&signal_index="+str(signal_index+1)+""+"'"+';"> + </button>'
    
    
    
    
    string =string+buttonstring_prev+buttonstring_next+buttonstring_up+buttonstring_down
    with open(files[sample_index][:-4]+".hea") as headerfile:
        cont=headerfile.read()
        paragraphs=cont.split("\n\n")
        string+="<p>"+paragraphs[2]+"</p>"

    y=ingest.ptbdiagnostic.curve_from_file_ptb(files[sample_index],12,signal_index-1)[:7000]
    return string, y

def int_request_argument(name:str,default):
    arg=flask.request.args.get(name)
    if not arg:
        arg=default
    else:
        arg=int(arg)
    return arg
    
