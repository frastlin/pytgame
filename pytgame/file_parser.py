import os, sys
import app
from game_object import default_object

def create_data(data_files='data/', component_files=None, data_ext='.dat'):
	"""populates the child_list of app.default_object with objects in the data files in the data_files dir."""
	if not component_files:component_files = data_files + 'components/'
	component_files = component_files.replace('/', '\\')
	if not component_files.startswith('\\'):component_files = '\\' + component_files
	sys.path.append(os.getcwd() + component_files)
	file_list = os.listdir(data_files)
	file_list = [data_files + f for f in file_list if f.endswith(data_ext)]
	parse_files(file_list)

def parse_files(file_list):
	objects = {}
	for file in file_list:
		d = {}
		execfile(file, globals(), d)
		for k, v in d.items():
			if hasattr(v, "isgameobject") and v.isgameobject():
				objects[k] = v
	default_object.add_children(**objects)


