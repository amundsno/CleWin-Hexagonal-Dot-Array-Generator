import numpy as np

def get_dot_array(diameter: int, pitch: int, btm_left_corner: tuple, top_right_corner: tuple, filter_functions: list) -> list:
    """Returns a list of tuples (x, y, diameter) describing the hexagonal dot array pattern.
    
    :param diameter: diameter of dots in µm
    :param pitch: pitch between dots in µm

    :param btm_left_corner: tuple (x, y) describing the bottom left corner coordinates to iterate from to create the hexagonal array
    :type btm_left_corner: tuple(int, int) [µm]
    
    :param top_right_corner: tuple (x, y) describing the top right corner coordinates to iterate to to create the hexagonal array
    :type top_right_corner: tuple(int, int) [µm]

    :param filter_functions: list of filter functions
    :type filter_functions: list(filter_func)
    
    :param filter_func: takes (x, y, diameter) [nm] describing (x, y) centre coordinates of a single dot with given diameter. Returns True if the dot is to be added to the array, and False if not.
    :type filter_func: function -> bool
    """
    
    # CleWin .cif-file uses 0.001 µm = 1 nm as the base unit.
    # Have to multiply µm values by 1000. No commas allowed.
    diameter           *= 1000
    pitch              *= 1000
    btm_left_corner     = tuple(i*1000 for i in btm_left_corner)
    top_right_corner    = tuple(i*1000 for i in top_right_corner)
    
    # Convenience variables for calculating hexagonal grid centres
    sin60 = np.sqrt(3)/2
    psin60 = int(np.round(pitch*sin60, 0))
    
    # Counter variables
    x, y = btm_left_corner
    row_counter = 1

    # Iterate over square area and calculate dot cetres
    dot_array = []
    while y < top_right_corner[1]:
        x = btm_left_corner[0]
        if row_counter % 2 == 0:
            x += psin60
        while x < top_right_corner[0]:
            # Apply all filter functions
            if all([filter_func(x, y, diameter) for filter_func in filter_functions]):
                dot_array.append((x,y, diameter))
            x += 2*psin60
        y += pitch/2
        row_counter += 1

    return dot_array

def write_to_cif(dot_array: list, layer_name: str, read_filepath: str, write_filepath: str):
    """Converts the dot_array to a .cif-format and writes it to the write_filepath

    :param dot_array: List of tuples (x, y, diameter) describing the hexagonal dot array pattern
    :param layer_name: Name of CleWin-layer to write to
    :param read_filepath: Path to CleWin .cif-file to use as blank/template. Design already in the file will be preserved. Use a new .cif-file if it is not needed.
    :param write_filepath: Path to CleWin .cif-file to write the array to. Will be created if it does not exist.

    NOTE: Remember to use the same path for read_filepath and write_filepath if multiple writes are needed. Otherwise only the final write will be saved.
    """
    print(f"Writing hexagonal dot array pattern to layer \"{layer_name}\" in \"{write_filepath}\"... ", end='')

    with open(read_filepath, "r") as file:
        read_content = file.read()

    cif_format_dot_array = f'L {layer_name};\n'
    for dot in dot_array:
        cif_format_dot_array += f'R {dot[2]} {dot[0]} {dot[1]};\n'

    write_content = read_content.split('DF;\n')
    write_content.insert(1, cif_format_dot_array + 'DF;\n')
    write_content = ''.join(write_content)

    with open(write_filepath, "w") as file:
        file.write(write_content)
    
    print("Done!")