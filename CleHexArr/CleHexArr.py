"""
## CleHexArr
    
CleHexArr is a simple module for generating and writing hexagonal arrays of circles to CleWin's .cif-filetype. 

Refer to the [README.md](https://github.com/amundsno/CleWin-Hexagonal-Dot-Array-Generator) as well as each function's docstring for documentation.

---

#### Quick usage example
>>> from CleHexArr import CleHexArr, Filters
>>> circle_filter = Filters.is_in_circle(0, 0, 100)
>>> circle_array = CleHexArr.generate_hexagonal_array(
...     diameter = 5,
...     pitch = 10,
...     x0 = -100, x1 = 100,
...     y0 = -100, y1 = 100, 
...     filter_functions = [circle_filter]
... )
>>> CleHexArr.write_array(
...     circle_array,
...     writepath = 'example.cif',
...     readpath = 'blank.cif',
...     layer = 'L0'
... )
"""

from dataclasses import dataclass
from typing import Callable
import numpy as np
import os

FilterFunctionType = Callable[[float, float, float], bool]

__all__ = [
    "generate_hexagonal_array",
    "write_array"
]

def generate_hexagonal_array(diameter: float, pitch: float, x0: float, x1: float, y0: float, y1: float, filter_functions: list[FilterFunctionType] = []) -> list[float]:
    """
    Generates hexagonal array of circles. All units are in ``µm``.
    
    ---
    Parameters:
    - `diameter``               : Circle diameters
    - `pitch``                  : Space between circle centers)
    - `x0`, `x1`, `y0`, `y1`    : Coordinates bounding area to be filled with circles
    - `filter_functions`        : List of boolean functions taking (x, y, diameter) of a circle to determine whether it is to be placed or not (True/False). See examples in the ``Filters`` module.
    """
    
    # Convenience variables for calculating hexagonal grid centres
    sin60 = np.sqrt(3)/2
    psin60 = pitch*sin60
    
    if x0  > x1:
        x0, x1 = x1, x0
    if y0 > y1:
        y0, y1 = y1, y0
    
    # Counter variables
    x, y = x0, y0
    row_counter = 1
    
    # Iterate over square area and calculate dot centers
    circles = []
    while y < y1:
        x = x0
        if row_counter % 2 == 0:
            x += psin60
        while x < x1:
            # Apply all filter functions
            if all([filter_func(x, y, diameter) for filter_func in filter_functions]):
                circles.append((x,y, diameter))
            x += 2*psin60
        y += pitch/2
        row_counter += 1
    
    return circles

def _array_2_CIF(circles: list[float]) -> str:
    """
    Converts array of circles to the .cif-file format
    """
    cif_content = ''
    for circle in circles:
        # CleWin .cif-file uses 0.001 µm = 1 nm as the base unit. No commas allowed.
        x, y, diameter = [int(np.round(entry*1000)) for entry in circle]
        cif_content += f'R {diameter} {x} {y};\n'
            
    return cif_content
    
def write_array(circles: list[float], writepath: str, readpath: str = '', layer: str = 'L0'):
    """
    Writes/inserts the array of circles into a CleWin .cif-file.

    ---
    Parameters:
    - ``writepath``         : Filepath to write to. Will be created with ``blank.cif`` as base if the path does not exist.
    - ``readpath``          : Filepath to read from. Unspecified by deafult, assuming readpath = writepath. To use blank set equal to ``blank.cif``
    - ``layer``             : Name of layer to write to (CleWin defaults are L0, L1, L2, etc.).
    """
    use_blank = False
    
    if readpath == '':
        if os.path.exists(writepath):
            readpath = writepath
        else:
            use_blank = True
    
    if readpath == 'blank.cif':
        use_blank = True
    
    if use_blank:
        read_content = \
            """
            (CIF written by CleWin 4.1);
            (1 unit = 0.001 micron);
            (Layer names:);
            L L0; (CleWin: 0 0 Layer 0/0f808000 0f808000);
            (Top level:);
            DS1 1 10;
            9 MainSymbol;
            DF;
            C 1;
            E
            """
    else:
        try:
            # Comment below can be used to get path to 'blank.cif' in repository
            # readpath = os.path.realpath(__file__).replace('\\CleHexArr\\CleHexArr.py', '\\blank.cif')
            with open(readpath, "r") as file:
                read_content = file.read()
        except FileNotFoundError as e:
            print('==============================================================================')
            print('ERROR! File not found!')
            print(f'Could not find readpath: {readpath}')
            print('Make sure the correct path is given, or use readpath=\'blank.cif\' to use the blank file.')
            print('==============================================================================')
            exit()
            
    cif_content = f'L {layer};\n'
    cif_content += _array_2_CIF(circles)

    write_content = read_content.split('DF;\n')
    write_content.insert(1, cif_content + 'DF;\n')
    write_content = ''.join(write_content)

    with open(writepath, "w") as file:
        file.write(write_content)