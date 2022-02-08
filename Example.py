from CleHexArr import CleHexArr, Filters

# EXAMPLE 1
# ====================================================================================================
N_bands         = 3
band_width      = 100
gap_width       = 100
d0, dx          = 5, 5

circles = []
for i in range(N_bands):
    di      = d0 + i*dx
    p       = di * 2
    R_outer = (band_width + gap_width)*(i+1)
    R_inner = band_width*i + gap_width*(i+1)
    
    circles += CleHexArr.generate_hexagonal_array(
        di,
        p,
        -R_outer, R_outer, -R_outer, R_outer,
        [
            Filters.is_not_in_circle(0, 0, R_inner),
            Filters.is_in_circle(0, 0, R_outer)
        ]
    )

CleHexArr.write_array(circles, 'example_1.cif', 'blank.cif', 'L0')
# ====================================================================================================

# EXAMPLE 2
# ====================================================================================================
R = 600                             # Radius of center circle filter
x0, x1, y0, y1 = -R, R, -R, R       # Boundaries of hexagonal pattern

my_circle_filter_center = Filters.is_in_circle(0, 0, R)
my_circle_filter_custom = Filters.is_in_circle(-300, 300, 200)

diameters   = [5, 10, 15]
pitches     = [d*3 for d in diameters]

circles     = []

circles += CleHexArr.generate_hexagonal_array(
    diameters[0],
    pitches[0],
    x0, x1, y0, y1,
    [my_circle_filter_custom]
)

circles += CleHexArr.generate_hexagonal_array(
    diameters[1],
    pitches[1],
    x0, x1, y0, y1,
    [my_circle_filter_center, Filters.is_in_top_right_quadrant, Filters.is_not_in_x_range(100, 150)]
)

circles += CleHexArr.generate_hexagonal_array(
    diameters[2],
    pitches[2],
    x0, x1, y0, y1,
    [my_circle_filter_center, Filters.is_in_btm_left_quadrant, Filters. is_not_in_y_range(-300, -200)]
)

CleHexArr.write_array(circles, 'example_2.cif', 'blank.cif', 'L0')
# ====================================================================================================