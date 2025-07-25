# import packages
import argparse
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path
import numpy as np
import os
import glob
import pandas as pd
import xml.etree.ElementTree as et
import datetime
from skimage.io import imread, imsave
from imageio import volread as imread
import tifffile
import sys
from skimage.external.tifffile import TiffWriter
#from tifffile import TiffWriter
import h5py
from skimage.transform import pyramid_reduce
from skimage.util import img_as_float, img_as_uint
import skimage.io as io

#argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-wild_card")
parser.add_argument("-NUM_FOVS")
args = parser.parse_args()

wild_card = args.wild_card
NUM_FOVS = args.NUM_FOVS

#print(wild_card)

# Convert the ims file to a tif with no downsampling performed
def convert_to_tif(f_name, new_f_name):
    read_file = h5py.File(f_name)
    base_data = read_file['DataSet']

    # THIS ASSUMES THAT YOU HAVE A MULTICOLOR Z STACK IN TIME
    resolution_levels, \
    time_points, n_time_points, \
    channels, n_channels, \
    n_z_levels, z_levels, \
    n_rows, n_cols = get_h5_file_info(base_data)

    # Get the index of the bad frame start
    bad_index_start = get_bad_frame_index(np.array(base_data[resolution_levels[0]][time_points[0]][channels[0]]['Data']))

    banner_text = 'File Breakdown'
    print(banner_text)
    print('_'*len(banner_text))
    print('Channels: %d' % n_channels)
    print('Time Points: %d' % n_time_points)
    print('Z Levels: %d' % (bad_index_start+1))
    print('Native (rows, cols): (%d,%d)'%(n_rows, n_cols))
    print('_'*len(banner_text))

    with TiffWriter(new_f_name, imagej=True) as out_tif:
        mmap_fname = f_name+'.mmap'
        output_stack = np.memmap(mmap_fname, dtype=np.uint16, shape=(n_time_points, bad_index_start, n_channels, n_rows, n_cols), mode='w+')

        for i_t, t in enumerate(time_points):
            print('%s/%d'%(t,n_time_points-1))
            for i_z, z_lvl in enumerate(z_levels[:bad_index_start]):
                print('%s/%d Z %d/%d'%(t, n_time_points-1, i_z+1, bad_index_start))
                for i_channel, channel in enumerate(channels):
                    output_stack[i_t, i_z, i_channel] = img_as_uint(np.array(base_data[resolution_levels[0]][time_points[i_t]][channels[i_channel]]['Data'][i_z]))

        # Save the reduced file
        out_tif.save(output_stack)

        # Delete the reduced stack
        del output_stack
        os.remove(mmap_fname)

def get_h5_file_info(h5_dataset):
    # Get a list of all of the resolution options
    resolution_levels = list(h5_dataset)
    resolution_levels.sort(key = lambda x: int(x.split(' ')[-1]))

    # Get a list of the available time points
    time_points = list(h5_dataset[resolution_levels[0]])
    time_points.sort(key = lambda x: int(x.split(' ')[-1]))
    n_time_points = len(time_points)

    # Get a list of the channels
    channels = list(h5_dataset[resolution_levels[0]][time_points[0]])
    channels.sort(key = lambda x: int(x.split(' ')[-1]))
    n_channels = len(channels)

    # Get the number of z levels
    n_z_levels = h5_dataset[resolution_levels[0]][time_points[0]][channels[0]][
                   'Data'].shape[0]
    z_levels = list(range(n_z_levels))

    # Get the plane dimensions
    n_rows, n_cols = h5_dataset[resolution_levels[0]][time_points[0]][channels[0]][
                   'Data'].shape[1:]

    return resolution_levels, time_points, n_time_points, channels, n_channels, n_z_levels, z_levels, n_rows, n_cols

def get_bad_frame_index(first_time_point):
    # Now go back through the frames looking for the zeros
    # Find the index of the first zero-frame.
    # Don't know why this bug exists, but it does, so have to deal.
    # Compensate for single z-level stacks that don't need bad frame search.
    if first_time_point.shape[0] == 1:
        return 1
    first_bad_frame_index = first_time_point.shape[0] - 1
    for i_z in range(first_time_point.shape[0])[::-1]:
        if not first_time_point[i_z].any():
            first_bad_frame_index = i_z
    return first_bad_frame_index


# next make the empty files for outpur destination
make_tif_file = "mkdir tif"
os.system(make_tif_file)

make_empty_files = f"for file in *{wild_card}*;" + "do mkdir tif/${file}; done"
os.system(make_empty_files)

# convert to tiff
cycles = glob.glob(f'*{wild_card}*') 
error_files = []
for i in cycles:
    #print(i)
    ims = glob.glob(f'{i}/*')
    for file in ims:
        try:
            sourceFile = file
            destFile = "tif/" + file[:-4]+'.tif'
            print(destFile)
            #print(destFile)
            convert_to_tif(sourceFile, destFile)
        except:
            print(f'{i} has B-tree error or import error')
            error_files.append(file)
            pass
