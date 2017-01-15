from collections import OrderedDict
#the command dictionaries
aliases = OrderedDict({})
admin = OrderedDict({})
movement = OrderedDict({})
verbs = OrderedDict({})
misc = OrderedDict({})

commands = [aliases, admin, movement, verbs, misc]

def clear_commands(dict_name, *commands):
	if args:
		[del(globals()[dict_name][c] for c in args]
	else:
		globals()[dict_name].clear()

def register(command, func=None, dictionary=misc):
	"""Call this with either the command as a string or with a decorator. If using it as a decorator, give the dictionary first. Take a look at north below. If one didn't use the decorator it would look like: add('north', north, top_verbs). One can also pass a func in without any argument and the default current_room will show."""
	if not func:
		if hasattr(command, '__call__'):
			dictionary[command.__name__] = command
			return

		def add_func(f):
			d, c = (command, f.__name__)
			d[c] = f
		return add_func
	else:
		dictionary[command] = func

from events import trigger
@register
def quit(a):
	"""quits the session"""
	trigger('on_quit')
