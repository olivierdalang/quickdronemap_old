import math

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