#!/usr/bin/env python

def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def clamp(x, out_min, out_max):
    return max(min(x,out_min),out_max)
