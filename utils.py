import os, math, json

import PIL

import numpy as np

def gps_tag_to_decimal_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)

def absolute_angle_difference(b1, b2):
    # Adapted from https://rosettacode.org/wiki/Angle_difference_between_two_bearings#Python
    r = (b2 - b1) % math.pi*2.0
    if r >= math.pi:
        r -= math.pi*2.0
    return abs(r)

def resized(img_path, factor=0.25):
    """Given an input path, returns a scaled image path"""

    filename = os.path.basename(img_path) + '.resized.{}.jpg'.format(factor)
    output_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
    if not os.path.exists(output_path):
        img = PIL.Image.open(img_path)
        img = img.resize((round(img.size[0]*factor), round(img.size[1]*factor)), PIL.Image.ANTIALIAS)
        img.save(output_path)
    return output_path


def transform_matrix(scale, angle, tvec):
    s = scale
    cosA, sinA = math.cos(angle), math.sin(angle)
    dx, dy = tvec
    mtrx_scale = np.matrix([
        [s, 0, 0],
        [0, s, 0],
        [0, 0, 1],
    ])
    mtrx_rotate = np.matrix([
        [cosA, -sinA, 0],
        [sinA,  cosA, 0],
        [0,     0,    1],
    ])
    mtrx_offset = np.matrix([
        [1,0,dx],
        [0,1,dy],
        [0,0,1 ],
    ]) 
    return mtrx_rotate * mtrx_scale * mtrx_offset