# cvee

A set of tools for CV researchers.

## Installation

### Install locally

```bash
pip install -e .
```

## Coordinate convention

- Camera Pose is the camera-to-world transformation while extrinsic is the world-to-camera transformation.
- Axes direction of different coordinates:
    - World coord: x -> front, y -> left, z -> up (right-handed)
    - OpenCV coord: x -> right, y -> down, z -> front (right-handed)
    - OpenGL coord: x -> right, y -> up, z -> back (right-handed)
    - Pixel coord: x -> down, y -> right (upper-left corner is [0, 0], lower-right corner is [width-1, height-1])
- Camera intrinsic, extrinsic and pose are defined in OpenCV coordinate.

## Acknowledgement

Some code is adapted from [mmcv](https://github.com/open-mmlab/mmcv/) and [detectron2](https://github.com/facebookresearch/detectron2/).