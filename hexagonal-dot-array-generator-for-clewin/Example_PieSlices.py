from HexDotArrayFunctions import get_dot_array, write_to_cif
from FilterFunctions import is_in_top_right_quadrant, is_in_btm_right_quadrant, is_not_in_200um_centre_cross_region, is_inside_8mm_Ø_circle
import numpy as np

# USER_INPUT
# ===================================================
# File and layer names
layer_name      = 'DotArray'
blank_filepath  = '8mm_pie_template.cif'
write_filepath  = '8mm_pie_design_0.cif'

# Top right quadrant parameters
diameter_1      = 30
pitch_1         = 90

# Bottom right quadrant parameters
diameter_2      = 50
pitch_2         = 120
# ===================================================

# Hexagonal pattern inside circle in top right quadrant
filters_1 = [
    is_in_top_right_quadrant, 
    is_not_in_200um_centre_cross_region, 
    is_inside_8mm_Ø_circle
    ]
dot_array = get_dot_array(diameter_1, pitch_1, (0,0), (4000, 4000), filters_1)
write_to_cif(dot_array, layer_name, blank_filepath, write_filepath)

# To make sure further writes are stacked on top of each other
blank_filepath = write_filepath

# Hexagonal pattern inside circle in bottom right quadrant
filters_2 = [
    is_in_btm_right_quadrant, 
    is_not_in_200um_centre_cross_region, 
    is_inside_8mm_Ø_circle
    ]
dot_array = get_dot_array(diameter_2, pitch_2, (0,-4000), (4000, 0), filters_2)
write_to_cif(dot_array, layer_name, blank_filepath, write_filepath)