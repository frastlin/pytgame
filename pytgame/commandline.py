from cmd import Cmd
from app import trigger
from lexicon_functions import *

class App_cmd(Cmd):

	def default(self, line):
		"""parseline breaks the line into command, arg, line. Then the getattr adds the string to the self with .."""
		command, arg, line = self.parseline(line)
		func = [getattr(self, n) for n in self.get_names() if n.startswith('do_' + command)]
		if len(func) == 1:
			return func[0](arg)
		print("I do not understand that command")

	def do_quit(self, a):
		"""triggers an on_quit event"""
		trigger("on_quit")

	def do_north(self, a):
		"""Moves the player north"""
		trigger('on_exit', ['north'])

	def do_south(self, a):
		"""Moves the player to the south"""
		trigger('on_exit', ['south'])

	def do_east(self, a):
		"""Moves the player east"""
		trigger('on_exit', ['east'])

	def do_west(self, a):
		"""Moves the player to the west"""
		trigger('on_exit', ['west'])

	def do_up(self, a):
		"""Moves the player upward"""
		trigger('on_exit', ['up'])

	def do_down(self, a):
		"""Moves the player down"""
		trigger('on_exit', ['down'])

	def do_shop(self, a):
		"""controlls the shop menu. Type shop, then the command for the shop like: shop list, shop identify, shop buy, shop sell..."""
		if not a:
			trigger('on_shop', [a])

	def do_look(self, a):
		"""Look by itself looks at the room, look with the object after it looks at an item"""
		trigger('on_look', [a])

	def do_take(self, a):
		"""Take an item from a container or from the ground"""
		trigger('on_take', [a])

	def do_drop(self, a):
		"""Transfer an item from your invintory to the ground"""
		trigger('on_drop', [a])

	def do_get(self, a):
		"""Works exactly like take, it transfers an item from the ground or a container to your invintory"""
		trigger('on_take', [a])
		trigger('on_get', [a])

	def do_inventory(self, a):
		"""Lists the items in your inv"""
		trigger('on_inventory', [])

	def do_say(self, a):
		"""outputs text to the screen"""
		print(self, a)
		trigger('on_say', [a])

	def do_tell(self, a):
		"""Tell a spacific person or creature something"""
		trigger('on_tell', [a])

	def do_close(self, a):
		"""Closes a container or door"""
		trigger('on_close', [a])

def add(command, func=None, dictionary=current_room):
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


def command(c):
	for d in commands:
		for k in d:
			if k.startswith(c):
				return d[k]
	return default

