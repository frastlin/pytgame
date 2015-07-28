#Go down to "all the commands" or search for do_ and you will find the commands
from cmd import Cmd
from time import sleep
import states
from events import trigger
from settings import fps

class App_cmd(Cmd):

	prompt = "\n>"

	def default(self, line):
		"""parseline breaks the line into command, arg, line. Then the getattr adds the string to the self with .."""
		command, arg, line = self.parseline(line)
		func = [getattr(self, n) for n in self.get_names() if n.startswith('do_' + command)]
		if len(func) == 1:
			return func[0](arg)
		print("I do not understand that command")

	def precmd(self, line):
		"""gives the event on_input"""
		trigger('on_input', [line])
		return line

	def postcmd(self, stop, line):
		"""First runs the wait_for_input_time, then returns the oppiset of states.running because when states.running is False that means that the program needs to end and stop should be True."""
		return True

	def __setattr__(self, attr, value):
		if attr not in dir(self):
			if attr == "__ordered_fields__":
				super.__setattr__(self, attr, value)
			else:
				if not hasattr(self, "__ordered_fields__"):
					setattr(self, "__ordered_fields__", [])
				self.__ordered_fields__.append(attr)
				super.__setattr__(self, attr, value)

#all the commands

	def do_quit(self, a):
		"""triggers an on_quit event by returning False"""
		trigger('on_quit')


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

if __name__ == '__main__':
	app = App_cmd()
	app.cmdloop()
