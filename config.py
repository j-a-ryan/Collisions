import math

import numpy as np

graph_area_color = "#E0FFFF" #"#FCFEE7"
graph_encasing_area_color = "#D6FFFF" # "#D1FFFF"# "#F2F3EA"
slider_accent_color = "#42A1FF" # "#4DA6FF" # 
slider_background_color = graph_area_color # "#D6FFFF" # "#D1FFFF"
graph_circles_color = "#272EF5"
graph_extra_circles_color = slider_accent_color
# Vector configuration, both model- and GUI-side
gui_vectors_header = ["t", "x", "y", "z", "name"]
max_num_vectors = 6
xyz_min = -10
xyz_max = 10
xyz_decimal_precision = 2
zero_rounding_tolerance = 1e-5
zero_rounding_tolerance_string = "1e-5"
form_field_invalid_color = "#FA0730"
field_invalid_stylestring = "color: white; background-color: #FF6347;"
combo_box_invalid_stylesheet = "QComboBox { " + field_invalid_stylestring + " }"
text_edit_invalid_stylesheet = "QLineEdit { " + field_invalid_stylestring + "; } QLineEdit:focus { color: red; background-color: PaleTurquoise; }"
exp_2yT = 2
sqrt2 = math.sqrt(2)
subtitle = "QCD/TMD"







def read_config_file():
    pass