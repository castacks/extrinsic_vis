# extrinsic_vis
A simple tool for visualizing calibrated extrinsics

# Prerequisites

```bash
pip3 install pyyaml pytransform3d
```

# How to use

```bash
python3 -m extrinsic_vis.draw_frames \
    ./extrinsic_vis/sample/daa_extrinsic_20221008/log1-camchain.yaml \
    --type kalibr \
    --vis-size 0.25
```

`--vis-size` controls the range of the plot. Unit is meter.

# Note

Currently, only Kalibr output is supported.

# Who to talk to

Yaoyu Hu \<yaoyuh@andrew.cmu.edu\>