
import argparse
import numpy as np
import matplotlib.pyplot as plt
import yaml

import matplotlib.pyplot as plt

from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager

from .reader import READERS

VALID_TYPES = READERS.keys()

def handle_args():
    global VALID_TYPES
    
    parser = argparse.ArgumentParser(description='Draw frames of calibrated system. ')
    
    parser.add_argument('infile', type=str, 
                        help='The input file containing the calibration data. ')
    parser.add_argument('--type', type=str, default='kalibr', 
                        choices=VALID_TYPES,
                        help='The type of the input file. Valid options are: kalibr, ros. ')
    
    return parser.parse_args()

def main():
    # Handle the arguments.
    args = handle_args()
    
    # Create the reader.
    reader = READERS[args.type]()
    
    # Read the calibration result.
    reader.read( args.infile )
    
    # Construct the transforms.
    tm = TransformManager()
    
    print(f'The extrinsics are: ')
    for cam_key, tf in reader.extrinsics.items():
        print(f'{cam_key}: \n{tf}')
        
        T_rig_sensor = pt.transform_from( tf[:3, :3], tf[:3, 3] )
        tm.add_transform( cam_key, 'rig', T_rig_sensor )

    ax = tm.plot_frames_in('rig', s=0.1)
    ax.set_ylim( (-0.25, 0.25) )
    ax.set_xlim( (-0.25, 0.25) )
    ax.set_zlim( (-0.25, 0.25) )
    plt.show()
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit( main() )