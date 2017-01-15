from pytgame import settings

class GameObject(object):
	def __init__(self, name="default_object"):
		self.name = name
		self.parent = None
		self.id = settings.id + 1
		self._child_list = []
		self._child_list_ids = {}
		self._child_list_names = {}
		#functions:
		settings.id += 1

	def init(self):
		self.on_init()
		[child.init() for child in self._child_list]

	def uninit(self):
		[child.uninit() for child in self._child_list]
		self.on_uninit()

	def on_init(self):
		pass

	def on_uninit(self):
		pass

	def add_child(self, child):
		child.parent = self
		if not hasattr(child, 'name'):child.name = "default_name"
		if self._child_list_names.get(child.name):self._child_list_names[child.name].append(child)
		else:self._child_list_names[child.name] = [child,]
		if not hasattr(child, 'id'):
			child.id = settings.id + 1
			settings.id += 1
		self._child_list.append(child)
		self._child_list_ids[child.id] = child
		return child

	def add_children(self, _children=[], **kwargs):
		if not _children:
			for k, v in kwargs.items():
				if not hasattr(v, 'name'):v.name = k
				_children.append(v)
		return [self.add_child(c) for c in _children]

	def get_child(self, id=0, name="", all_name=""):
		if id:
			return self._child_list_ids.get(id)
		if name:
			return self._child_list_names.get(name)[0]
		elif all_name:
			return self._child_list_names.get(all_name)

	def get_children(self, list=False, id=False, name=False):
		"""Returns either a list, dict with ids as the keys or dict with name as the key"""
		if list:return self._child_list
		elif id:return self._child_list_ids
		elif name:return self._child_list_names


default_object = GameObject('default_object')