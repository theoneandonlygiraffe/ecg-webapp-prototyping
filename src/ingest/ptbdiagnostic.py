import os
import struct

import numpy as np



def data_from_file_ptb(filepath):
    with open(filepath,"rb") as file:
        data_out=[]
        buffer=file.read(2)
        while buffer:
            num=struct.unpack("h",buffer)[0]
            data_out.append(num)
            buffer=file.read(2)
        return np.array(data_out)
        

def curve_from_file_ptb(filepath,num_curves,curve):
    data_raw=data_from_file_ptb(filepath)
    if len(data_raw)%num_curves:
        raise ValueError("error::curve_from_file_ptb("+filepath+","+num_curves+")::incorrect number of curves")

    out=[]
    
    for i in range(0,data_raw.size,num_curves):
        out.append(data_raw[i+curve])
    
    return np.array(out)

