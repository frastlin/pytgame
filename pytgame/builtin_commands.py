#These are all the built-in functions for moving, taking and everything related to commands for the prompt
import commands as _commands
from commands import register as _register
from events import trigger as _trigger
from printer import printer as _printer

def list_commands(with_help=False):
	"""Lists all commands in the module. If with_help, it will return a string with just the functions with help strings"""
	s = ""
	for d in _commands.commands:
		for k, v in d.items():
			if with_help and v.__doc__:
				s += v.__name__ + "\n"
			elif not with_help:
				s += v.__name__ + "\n"
	return s

@_register(_commands.admin)
def quit(a):
		"""triggers an on_quit event to exit the program"""
		_trigger("on_quit")

@_register(_commands.admin)
def commands(a):
	"""Just type commands to see a list of all commands. To see a list of all commands with a help function type commands help"""
	if a and a[0] in 'help':
		_printer("Here is a list of commands with a help topic:")
		_printer(list_commands(True))
	else:
		_printer("Here is a list of all commands:")
		_printer(list_commands())

@_register(_commands.movement)
def north(a):
	"""Moves the player north"""
	_trigger('on_exit', ['north'])

@_register(_commands.movement)
def south(a):
	"""Moves the player to the south"""
	_trigger('on_exit', ['south'])

@_register(_commands.movement)
def east(a):
	"""Moves the player east"""
	_trigger('on_exit', ['east'])

@_register(_commands.movement)
def west(a):
	"""Moves the player to the west"""
	_trigger('on_exit', ['west'])

@_register(_commands.movement)
def up(a):
	"""Moves the player upward"""
	_trigger('on_exit', ['up'])

@_register(_commands.movement)
def down(a):
	"""Moves the player down"""
	_trigger('on_exit', ['down'])

@_register(_commands.verbs)
def shop(a):
	"""controlls the shop menu. Type shop, then the command for the shop like: shop list, shop identify, shop buy, shop sell..."""
	_trigger('on_shop', [a])

@_register(_commands.verbs)
def look(a):
	"""Look by itself looks at the room, look with the object after it looks at an item"""
	_trigger('on_look', [a])

@_register(_commands.verbs)
def take(a):
	"""Take an item from a container or from the ground"""
	_trigger('on_take', [a])

@_register(_commands.verbs)
def drop(a):
	"""Transfer an item from your invintory to the ground"""
	_trigger('on_drop', [a])

@_register(_commands.verbs)
def get(a):
	"""Works exactly like take, it transfers an item from the ground or a container to your invintory"""
	_trigger('on_take', [a])
	_trigger('on_get', [a])

@_register(_commands.verbs)
def inventory(a):
	"""Lists the items in your inventory"""
	_trigger('on_inventory', [])

@_register(_commands.verbs)
def say(a):
	"""Say something to the room by typing say followed by your text"""
	print(a)
	_trigger('on_say', [a])

@_register(_commands.verbs)
def tell(a):
	"""Tell a spacific person or creature something. Type tell followed by your text"""
	_trigger('on_tell', [a])

@_register(_commands.verbs)
def close(a):
	"""Closes a container or door"""
	_trigger('on_close', [a])
