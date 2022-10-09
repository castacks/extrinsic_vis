
import json
import numpy as np
import yaml

IDENTITY_TRANSFORM = np.eye(4, dtype=np.float64)

READERS = dict()

def register_reader(name):
    def register(cls):
        global READERS
        READERS[name] = cls
        return cls
    return register

def inv_transform(tf):
    R = tf[:3, :3]
    t = tf[:3,  3]
    res = np.eye(4, dtype=np.float64)
    res[:3, :3] = R.transpose()
    res[:3,  3] = -R.transpose().dot(t)
    return res

class ExtrinsicReader(object):
    def __init__(self, name):
        super().__init__()

        self.name = name
        self.extrinsics = None
        
    def read(self, fn):
        raise NotImplementedError()
    
    def __len__(self):
        return len(self.extrinsics)
    
    # This function is meant to be overwritten by the derived classes. 
    def int_idx_2_key(self, idx):
        return idx
    
    def __getitme__(self, key):
        if isinstance(key, int):
            key = self.int_idx_2_key(key)
        return self.extrinsics[key]

@register_reader('kalibr')
class KalibrReader(ExtrinsicReader):
    def __init__(self):
        super().__init__('Kalibr')
        
        # This overwrites the parent class' initial value.
        self.extrinsics = dict()
        
    def read(self, fn):
        print(f'{self.name}: Parsing {fn}...')
        
        with open(fn, 'r') as fp:
            data = yaml.load(fp, Loader=yaml.FullLoader)
            
        # Try to retrieve the extrinsics for all the cameras.
        idx = 0
        pre_cam_tf = None
        try:
            while True:
                cam_name = self.int_idx_2_key(idx)
                
                # Get the dictionary.
                cam = data[cam_name]
                
                # Test if T_cn_cnm1 key exists.
                if 'T_cn_cnm1' in cam.keys():
                    calib_tf = np.array(cam['T_cn_cnm1'], dtype=np.float64)
                    tf = pre_cam_tf @ inv_transform( calib_tf )
                else:
                    tf = IDENTITY_TRANSFORM
                    
                # Save the extrinsics.
                self.extrinsics[cam_name] = tf
                
                # Shown info.
                print(f'{cam_name}')
                
                # Prepare for the next iteration.
                pre_cam_tf = tf
                idx += 1
        except KeyError:
            pass
        
    def int_idx_2_key(self, idx):
        return f'cam{idx}'
    
@register_reader('plain_json')
class PlainJsonReader(ExtrinsicReader):
    def __init__(self):
        super().__init__('PlainJson')
        
        # This overwrites the parent class' initial value.
        self.extrinsics = dict()
        
    def read(self, fn):
        # Read the JSON file.
        with open(fn, 'r') as fp:
            j_obj = json.load(fp)
            
        # Get the "cameras" key.
        # Should be a list of dictionaries.
        cameras = j_obj['cameras']
        
        # Loop over all the cameras.
        for cam in cameras:
            raw_tf = np.array( cam['extrinsics']['T'], dtype=np.float64 )
            
            tf = inv_transform(raw_tf) \
                if cam['extrinsics']['frame_1'] == 'rig' \
                else raw_tf
            
            self.extrinsics[ cam['name'] ] = tf
