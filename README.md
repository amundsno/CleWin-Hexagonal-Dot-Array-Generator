# Hexagonal Dot Array Generator for CleWin (CleHexArr)
This repository contains a simple python module for creating hexagonal arrays of circles with a specified diameter and pitch in CleWin's .cif-file format. See ``Example.py`` and read the docstrings for documentation.

---

### Quick usage example
```python
from CleHexArr import CleHexArr, Filters

# Filter functions are used to further specify where circles are allowed in the hexagonal array.
circle_filter = Filters.is_in_circle(0, 0, 100)

circle_array = CleHexArr.generate_hexagonal_array(
    diameter = 5,
    pitch    = 10,
    x0 = -100, x1 = 100,
    y0 = -100, y1 = 100, 
    filter_functions = [circle_filter]
)

CleHexArr.write_array(
    circle_array,
    writepath = 'quick_example.cif',
    readpath = 'blank.cif',
    layer = 'L0'
)
```
![image](https://user-images.githubusercontent.com/24915157/153081294-a2cf249c-59c6-41bf-b428-498f1458c6dd.png)

---

## Output from `Example.py`

### Example 1
![image](https://user-images.githubusercontent.com/24915157/153078281-6ea6d8a6-8d42-4449-b058-10d96ffa32ae.png)

### Example 2
![image](https://user-images.githubusercontent.com/24915157/153078413-71ab252f-a078-437d-8cda-7aad787fe9bf.png)
