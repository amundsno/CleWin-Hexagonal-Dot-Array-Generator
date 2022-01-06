"""
Filter functions should take arguments:
    - ``x``, ``y``      - dot centre coordinates in ``µm``
    - ``diameter``      - dot diameter in ``µm``

Filter functions should return: 
    - ``True``  if the dot is to be added to the dot array, and
    - ``False`` if not
"""

import numpy as np

# QUADRANTS
# ---------

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

# CIRCLE
# ------
def is_in_circle(X, Y, R):
    """Returns filter function that only allows circles within circle with center (X, Y) and radius R."""
    return lambda x, y, diameter : (x-X)**2 + (y-Y)**2 < (R-diameter/2)**2

# RANGES
# ------
def is_not_in_x_range(X0, X1):
    if X0 > X1:
        X0, X1 = X1, X0
    return lambda x, y, diameter : (x + diameter/2) < X0 or (x - diameter/2) > X1

def is_not_in_y_range(Y0, Y1):
    if Y0 > Y1:
        Y0, Y1 = Y1, Y0
    return lambda x, y, diameter : (y + diameter/2) < Y0 or (y - diameter/2) > Y1

def is_not_in_center_cross(cross_width):
    """Returns filter functions that does not allow circles inside center cross area."""
    R = cross_width/2
    X_range = is_not_in_x_range(-R, R)
    Y_range = is_not_in_y_range(-R, R)
    return lambda x, y, diameter : X_range(x, y, diameter) and Y_range(x, y, diameter)