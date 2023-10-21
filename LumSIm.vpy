# Author: Mitchel Stewart <quackdoctech@gmail.com>
# vim: syntax=python
import vapoursynth as vs
import colour
#import vsutil
import numpy as np
import mvsfunc as mvf
import functools
import csv

core = vs.core
core.num_threads=1
core.max_cache_size = 65535


clip = core.lsmas.LWLibavSource(source='1kn.png')
clip = core.resize.Bicubic(clip=clip, format=vs.RGB48)

def lumpy(n, clip):
    csvfile="lum.csv"
    #image = colour.io.convert_bit_depth(image, "uint16") #needed for some buggy stuff
    vsframe = clip.get_frame(n)
    nparray = np.asarray(vsframe)
    image = np.dstack(nparray)
    
    BT2020 = colour.models.RGB_COLOURSPACE_BT2020.matrix_RGB_to_XYZ ##constants
    RGB_lin = colour.models.eotf_ST2084(image / 65535) #convert to PQ linear RGB #1023 for 10bit #65536  for 16bit
	#RGB_lin = colour.models.eotf_BT2100_HLG(image / 65535)
    xyz = colour.algebra.vector_dot(BT2020, RGB_lin)

    lum = xyz[:,:,1]
    average_lum = np.mean(lum)
    ninfifth = np.percentile(lum, 95)
    ninninth = np.percentile(lum, 99)
    peak = np.amax(lum)
    fifth = np.percentile(lum, 5)

    print("Average:", average_lum)
    print("95th:   ", ninfifth)
    print("99th:   ", ninninth)
    print("peak:   ", peak)
    print("5th:    ", fifth)
    print("frame:", n)
    #TODO: Add header
    #field_names = ['frame','average','95th','99th']
    #dict = {'frame':n, 'average':average_lum, '95th':ninfifth, '99th':ninninth}
    #with open("lum.csv", 'a') as csv_file:
    #     dict_object = csv.DictWriter(csv_file, fieldnames=field_names)
    #     dict_object.writerow(dict)
    
    return clip

def test(n, clip):
    vsframe = clip.get_frame(n)
    nparray = np.asarray(vsframe)
    ndarray = np.dstack(nparray)

    print("thing:", n, ndarray)
    return clip

clip = core.std.FrameEval(clip, functools.partial(lumpy, clip=clip))
clip.set_output()