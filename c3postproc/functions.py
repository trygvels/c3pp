import math
import sys
import os
import time
import healpy as hp
from astropy.io import fits
import numpy as np

def h5handler(flags, command):
    filename = str(flags[0])
    signal = str(flags[1])
    min = int(flags[2])
    max = int(flags[3])
    outname = flags[-1]
    l = max-min
    
    import h5py     
    dats = []
    with h5py.File(filename, 'r') as f:
        for i in range(min,max+1):
            s = str(i).zfill(6)
            dats.append(f[s+"/"+signal][()])
    dats = np.array(dats)

    outdata = command(dats, axis=0)
    if "fits" in outname[-4:]: 
        hp.write_map(outname, outdata, overwrite=True)
    else:
        np.savetxt(outname, outdata)

def mean(flags):
    h5handler(flags, np.mean)

def stddev(flags):
    h5handler(flags, np.std)

    

def map2pdf(flags, png=False):
    from c3postproc.plotter import Plotter
    optn_flags = []
    map = flags[0]
    if len(flags) > 1:
        optn_flags = flags[1:]
    Plotter(map, optn_flags, png)

def map2png(flags):
    map2pdf(flags, png=True)

def readhdf(flags):
    filename = str(flags[0])
    signal = str(flags[1])
    type = str(flags[2])
    sample_min = str(flags[3]).zfill(6)
    sample_max = str(flags[4]).zfill(6)
    
    import h5py     
    with h5py.File(filename, 'r') as f:
        data = f[sample+"/"+signal+"/"+type].value

        