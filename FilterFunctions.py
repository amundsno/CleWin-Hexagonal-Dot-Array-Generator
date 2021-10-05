import numpy as np
# Filter functions take parameters:
# (x,y)     - dot centre coordinates in nm
# diameter  - dot diameter in nm

# Filter functions return: 
# True if the dot is to be added to the dot array, and
# False if not

# Quadrants
def is_in_top_right_quadrant(x, y, diameter) -> bool:
    r = int(np.ceil(diameter/2))
    return x-r > 0 and y-r > 0
    
def is_in_btm_right_quadrant(x, y, diameter) -> bool:
    r = int(np.ceil(diameter/2))
    return x-r > 0 and y+r < 0

def is_in_btm_left_quadrant(x, y, diameter) -> bool:
    r = int(np.ceil(diameter/2))
    return x+r < 0 and y+r < 0

def is_in_top_left_quadrant(x, y, diameter) -> bool:
    r = int(np.ceil(diameter/2))
    return x+r < 0 and y-r > 0

# Some custom filter functions
def is_inside_8mm_Ø_circle(x, y, diameter):
    """Makes sure design fits inside circle with diameter 8000 µm"""
    R = 4000 *1000                  # .cif-file base unit is 0.001 µm = 1 nm, thus need to multiply by 1000
    r = int(np.ceil(diameter/2))
    return x*x + y*y < (R-r)**2

def is_not_in_200um_centre_cross_region(x, y, diameter):
    """Does not allow dots closer than 100 µm to the 0-axes"""
    gap_from_axis = 100 *1000       # .cif-file base unit is 0.001 µm = 1 nm, thus need to multiply by 1000
    r = int(np.ceil(diameter/2))
    return (x-r > gap_from_axis or x+r < -gap_from_axis) and (y-r > gap_from_axis or y+r < -gap_from_axis)