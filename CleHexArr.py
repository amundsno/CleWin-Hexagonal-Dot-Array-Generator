from dataclasses import dataclass
from typing import Callable
import numpy as np

__all__ = [
    "CleHexArr"
    ]

FilterFunctionType = Callable[[float, float, float], bool]

# Blank .cif-file content to be used if writepath does not exist
BLANK_CONTENT = '(CIF written by CleWin 4.1);\n(1 unit = 0.001 micron);\n(Layer names:);\nL L0; (CleWin: 0 0 Layer 0/0f808000 0f808000);\n(Top level:);\nDS1 1 10;\n9 MainSymbol;\nDF;\nC 1;\nE'

@dataclass
class CleHexArr:
    """
    ## CleHexArr
    
    Dataclass for generating and writing hexagonal arrays of circles to CleWin's .cif-filetype. 
    
    All arguments are in `µm`. Smallest allowed unit is `0.001 µm (1 nm)`.
    
    ---
    
    ### Available methods:
    - `addArray(...)` - Called in constructor. Multiple arrays can be generated and stored by the same object.
    - `write(...)` - Writes all stored arrays in .cif-format to specified path.
    
    See each method's docstring for documentation.
    """
    def __init__(self):
        """    
        Use the ``addArray(...)`` method to generate hexagonal arrays.
        
        >>> myArrays = CleHexArr()
        >>> myArrays.addArray(...)
        """
        self.arrays = []
        
    def addArray(self, diameter: float, pitch: float, x0: float, x1: float, y0: float, y1: float, filter_functions: list[FilterFunctionType] = []):
        """
        Generates hexagonal array of circles. All units are in µm.

        ---
        Parameters:
        - `diameter``               : Circle diameters
        - `pitch``                  : Space between circle centers)
        - `x0`, `x1`, `y0`, `y1`    : Coordinates bounding area to be filled with circles
        - `filter_functions`        : List of boolean functions taking (x, y, diameter) of a circle to determine whether it is to be placed or not (True/False). See examples in the ``Filters`` module.
        """
        
        # Convenience variables for calculating hexagonal grid centres
        sin60 = np.sqrt(3)/2
        psin60 = int(round(pitch*sin60, 3))
        
        if x0  > x1:
            x0, x1 = x1, x0
        if y0 > y1:
            y0, y1 = y1, y0
        
        # Counter variables
        x, y = x0, y0
        row_counter = 1
        
        # Iterate over square area and calculate dot centers
        dot_centers = []
        while y < y1:
            x = x0
            if row_counter % 2 == 0:
                x += psin60
            while x < x1:
                # Apply all filter functions
                if all([filter_func(x, y, diameter) for filter_func in filter_functions]):
                    dot_centers.append((x,y))
                x += 2*psin60
            y += pitch/2
            row_counter += 1
        
        self.arrays.append({'diameter':diameter, 'pitch':pitch, 'centers':dot_centers})
    
    def write(self, writepath: str, readpath: str = '', layer: str = 'L0', use_blank: bool = False, silent: bool = False):
        """
        Writes/inserts all arrays into a CleWin .cif-file.
        
        ---
        Parameters:
        - ``writepath``         : Filepath to write to. Will be created if it does not exist.
        - ``readpath``          : Filepath to read from. Unspecified by deafult, assuming readpath = writepath.
        - ``layer``             : Name of layer to write to (CleWin defaults are L0, L1, L2, etc.).
        - ``use_blank``         : False by default. Create new file instead of writing over write-/readpath.
        - ``silent``            : False by default. If True, no message will be printed when this function is called.
        """
                
        if not readpath:
            readpath = writepath
        
        try:
            if not use_blank:
                with open(readpath, "r") as file:
                    read_content = file.read()
            else:
                read_content = BLANK_CONTENT
        except FileNotFoundError:
            read_content = BLANK_CONTENT
        
        cif_hexarr_content = f'L {layer};\n'
        for i, arr in enumerate(self.arrays):

            if not silent:
                print(self._get_write_message(arr, layer, writepath))
                
            # CleWin .cif-file uses 0.001 µm = 1 nm as the base unit.
            # Have to multiply µm values by 1000. No commas allowed.
            diameter = int(arr['diameter']*1000)
            centers = np.array(arr['centers'])*1000
            centers = centers.astype(int)
            for center in centers:
                x, y = center[0], center[1]
                cif_hexarr_content += f'R {diameter} {x} {y};\n'
        
        write_content = read_content.split('DF;\n')
        write_content.insert(1, cif_hexarr_content + 'DF;\n')
        write_content = ''.join(write_content)

        with open(writepath, "w") as file:
            file.write(write_content)

        if not silent:
            print("Done!")
    
    def _get_write_message(self, array, layer, writepath):
        diameter    = array['diameter']
        pitch       = array['pitch']
        return f'Writing hexagonal dot array with d = {diameter} µm and p = {pitch} µm to layer "{layer}" in {writepath}...'
    
    def _get_layer_name(self, array):
        return f'd{array["diameter"]} p{array["pitch"]}'
    
    def __str__(self):
        return str(self.arrays)