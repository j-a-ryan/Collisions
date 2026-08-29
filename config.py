import math

graph_area_color = "#E0FFFF"  # "#FCFEE7"
graph_encasing_area_color = "#D6FFFF"  # "#D1FFFF"# "#F2F3EA"
slider_accent_color = "#42A1FF"  # "#4DA6FF" #
slider_background_color = graph_area_color  # "#D6FFFF" # "#D1FFFF"
graph_circles_color = "#272EF5"
graph_extra_circles_color = slider_accent_color
graph_tooltip_background_color = "#ffffe1"
# Vector configuration, both model- and GUI-side
# We use user-facing strings and simpler string for code-only usage.
# At some points there is a use of the former as keys in code-only usage, however.
vector_fields = ["t", "x", "y", "z", "name"]
gui_m2 = "m\u00b2"
gui_vectors_header = ["E", "p<sub>x</sub>", "p<sub>y</sub>", "p<sub>z</sub>", "name"]
gui_t = gui_vectors_header[0]
gui_x = gui_vectors_header[1]
gui_y = gui_vectors_header[2]
gui_z = gui_vectors_header[3]
gui_vector_name = gui_vectors_header[4]
lookup_gui_txyz_0123 = {gui_t: 0, gui_x: 1, gui_y: 2, gui_z: 3}
lookup_gui_0123_txyz = {"0": gui_t, "1": gui_x, "2": gui_y, "3": gui_z}
max_num_vectors = 6
boost_A_max = 10
xyz_min = -10
xyz_max = 10
t_max = 10  # t/E min is currently hardcoded as 0
xyz_decimal_precision = 2
zero_rounding_tolerance = 1e-5
zero_rounding_tolerance_string = "1e-5"
form_field_invalid_color = "#FA0730"
field_invalid_stylestring = "color: white; background-color: #FF6347;"
combo_box_invalid_stylesheet = "QComboBox { " + field_invalid_stylestring + " }"
text_edit_invalid_stylesheet = (
    "QLineEdit { " + field_invalid_stylestring + "; } QLineEdit:focus { color: red; background-color: PaleTurquoise; }"
)
exp_2yT = 1
sqrt2 = math.sqrt(2)
subtitle = "QCD/TMD"
particle_names = ["k1", "k2", "k3", "k4", "k5", "k6"]


def read_config_file():
    pass
