import numpy as np
import os
import glob
import pathlib  
import pandas as pd
from natsort import natsorted



def read_yolo_pose(path):
    with open(path, "r") as f:
        line = f.readline().strip().split()

    cls = int(line[0])
    cx, cy, bw, bh = map(float, line[1:5])

    kpts = list(map(float, line[5:]))

    return cls, cx, cy, bw, bh, kpts


def denormalize(cx, cy, bw, bh, kpts, w, h):
    cx *= w
    cy *= h
    bw *= w
    bh *= h

    keypoints = []
    for i in range(0, len(kpts), 3):
        x = kpts[i] * w
        y = kpts[i+1] * h
        v = kpts[i+2]
        keypoints.append([x, y, v])

    return cx, cy, bw, bh, keypoints


def split_left_yolo(cx, cy, bw, bh, keypoints, split_x):
    # bounding box corners
    x1 = cx - bw/2
    x2 = cx + bw/2

    # clip to LEFT
    x1 = max(0, x1)
    x2 = min(split_x, x2)

    new_bw = x2 - x1
    new_cx = (x1 + x2) / 2

    # filter keypoints
    new_kpts = []
    for x, y, v in keypoints:
        if x < split_x and not np.isnan(x):
            new_kpts.append([x, y, v])
        else:
            new_kpts.append([0, 0, 0])  # YOLO expects placeholder

    return new_cx, cy, new_bw, bh, new_kpts


def normalize_left(cx, cy, bw, bh, keypoints, split_x, h):
    cx /= split_x
    bw /= split_x
    cy /= h
    bh /= h

    kpts_norm = []
    for x, y, v in keypoints:
        if v == 0:
            kpts_norm.extend([0, 0, 0])
        else:
            kpts_norm.extend([x / split_x, y / h, v])

    return cx, cy, bw, bh, kpts_norm

def save_yolo_pose(cls, cx, cy, bw, bh, kpts, path):
    line = f"{cls} {cx} {cy} {bw} {bh} " + " ".join(map(str, kpts))
    with open(path, "w") as f:
        f.write(line + "\n")


def split_right_yolo(cx, cy, bw, bh, keypoints, split_x, w):
    # bounding box corners
    x1 = cx - bw / 2
    x2 = cx + bw / 2

    # clip to RIGHT
    x1 = max(split_x, x1)
    x2 = min(w, x2)

    new_bw = x2 - x1
    new_cx = (x1 + x2) / 2

    # filter keypoints
    new_kpts = []
    for x, y, v in keypoints:
        if v == 0:
            # 🔴 IMPORTANT: keep unchanged
            new_kpts.append([0, 0, 0])
        elif x >= split_x and not np.isnan(x):
            new_kpts.append([x, y, v])
        else:
            new_kpts.append([0, 0, 0])

    return new_cx, cy, new_bw, bh, new_kpts


def normalize_right(cx, cy, bw, bh, keypoints, split_x, w, h):
    crop_w = w - split_x

    cx = (cx - split_x) / crop_w
    bw = bw / crop_w
    cy /= h
    bh /= h

    kpts_norm = []
    for x, y, v in keypoints:
        if v == 0:
            # 🔴 preserve exactly
            kpts_norm.extend([0, 0, 0])
        else:
            kpts_norm.extend([(x - split_x) / crop_w, y / h, v])

    return cx, cy, bw, bh, kpts_norm