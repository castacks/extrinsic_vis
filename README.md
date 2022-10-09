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
    --format kalibr \
    --vis-size 0.25
```

- `--format` the format of the calibration file. See below.
- `--vis-size` controls the range of the plot. Unit is meter.

# Note

Currently, the support formats are
- __kalibr__: Kalibr yaml format. See ./sample/daa_extrinsic_20221008/log1-camchain.yaml for an example.
- __plain_json__: Plain JSON format. See ./sample/data_extrinsic_20221008/plain.json for an exmaple.

# Who to talk to

Yaoyu Hu \<yaoyuh@andrew.cmu.edu\>