from collections import OrderedDict
#the command dictionaries
admin = {}
movement = OrderedDict({})
verbs = OrderedDict({})
current_room = OrderedDict({})

commands = [admin, movement, verbs, current_room]

def register(command, func=None, dictionary=current_room):
	"""Call this with either the command as a string or with a decorator. If using it as a decorator, give the dictionary first. Take a look at north below. If one didn't use the decorator it would look like: add('north', north, top_verbs)"""
	if not func:
		def add_func(f):
			if hasattr(command, '__call__'):
				dictionary[command.__name__] = command
			d, c = (command, f.__name__)
			d[c] = f
		return add_func
	else:
		dictionary[command] = func
