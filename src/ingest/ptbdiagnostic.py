import os
import struct
import fnmatch

import numpy as np

from functools import lru_cache


@lru_cache(maxsize=5)
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


def find_files(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

@lru_cache(maxsize=2)
def find_files_type(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith( pattern):
                result.append(os.path.join(root, name))
    return result
