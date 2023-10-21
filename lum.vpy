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
clip = core.lsmas.LWLibavSource(source='hdr-jxl.png')
clip = core.resize.Bicubic(clip=clip, format=vs.RGB48)
#clip = core.resize.Bicubic(clip=clip, format=vs.RGB48, matrix_in_s="709", transfer=16)

def lumpy(n, clip):
    csvfile="lum.csv"
    #image = colour.io.convert_bit_depth(image, "uint16")
    vsframe = clip.get_frame(n)
    nparray = np.asarray(vsframe)
    image = np.dstack(nparray)

    BT2020 = colour.models.RGB_COLOURSPACE_BT2020.matrix_RGB_to_XYZ ##constants
    rgbf = image / 65535
    print("rgb float: \n",rgbf[600,600,:])
    RGB_lin = colour.models.eotf_ST2084(rgbf) #convert to PQ linear RGB #1023 for 10bit #65536 for 16bit
    print("RGB Linear:\n",RGB_lin[600,600,:])
    #RGB_lin = colour.models.eotf_BT2100_HLG(image / 65535)
    xyz = colour.algebra.vector_dot(BT2020, rgbf)
    

    lum = xyz[600,600,:]
    average_lum = np.mean(lum)
    ninfifth = np.percentile(lum, 95)
    ninninth = np.percentile(lum, 9)
    fifth = np.percentile(lum, 5)
    print("Xyz: \n",lum)
    print("\n")

	#print("value in nits;")
    print("Average:", average_lum)
    print("95th:   ", ninfifth)
    print("99th:   ", ninninth)
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