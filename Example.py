from CleHexArr import CleHexArr
from Filters import is_not_in_x_range, is_not_in_y_range, is_in_circle, is_in_top_right_quadrant, is_in_btm_left_quadrant

R = 500
x0, x1, y0, y1 = -R, R, -R, R

center_circle_filter = is_in_circle(0, 0, R)
my_circle_filter = is_in_circle(-200, 200, 100)

myArrays = CleHexArr()

myArrays.addArray(5, 15, x0, x1, y0, y1, [
    is_in_top_right_quadrant, 
    center_circle_filter, 
    is_not_in_x_range(50, 150)])

myArrays.addArray(10, 30, x0, x1, y0, y1, [
    is_in_btm_left_quadrant, 
    center_circle_filter, 
    is_not_in_y_range(-300, -200)])

myArrays.addArray(4, 12, x0, x1, y0, y1, [my_circle_filter])

myArrays.write('Example.cif')