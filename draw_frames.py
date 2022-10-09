
import argparse
import numpy as np
import matplotlib.pyplot as plt
import yaml

import matplotlib.pyplot as plt

from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager

from .reader import READERS

def handle_args():
    valid_types = READERS.keys()
    
    parser = argparse.ArgumentParser(description='Draw frames of calibrated system. ')
    
    parser.add_argument('infile', type=str, 
                        help='The input file containing the calibration data. ')
    parser.add_argument('--format', type=str, default='kalibr', 
                        choices=valid_types,
                        help=f'The type of the input file. Valid options are: {valid_types}. ')
    parser.add_argument('--vis-size', type=float, default=0.4, 
                        help='The size limit of the visualization. Unit: m. ')
    
    return parser.parse_args()

def main():
    # Handle the arguments.
    args = handle_args()
    
    # Create the reader.
    reader = READERS[args.format]()
    
    # Read the calibration result.
    reader.read( args.infile )
    
    # Construct the transforms.
    tm = TransformManager()
    
    print(f'The extrinsics are: ')
    for cam_key, tf in reader.extrinsics.items():
        print(f'{cam_key}: \n{tf}')
        
        T_rig_sensor = pt.transform_from( tf[:3, :3], tf[:3, 3] )
        tm.add_transform( cam_key, 'rig', T_rig_sensor )

    # Plot the frames.
    ax = tm.plot_frames_in('rig', s=0.1)
    ax.set_ylim( (-args.vis_size, args.vis_size) )
    ax.set_xlim( (-args.vis_size, args.vis_size) )
    ax.set_zlim( (-args.vis_size, args.vis_size) )
    plt.show()
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit( main() )