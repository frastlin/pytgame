import time
import states
import commands
import builtin_commands
from printer import printer
from events import trigger, add
from settings import fps

prompt = "\n>"
default = "I do not understand that command"
no_help = "There is no help for that command"
default_help = "Please type ? followed by the function name like:\n?take"

def run():
	while states.running:
		if states.input_time:
			trigger('on_input', [raw_input(prompt)])
			states.input_time = False
		else:
			time.sleep(fps)

@add
def on_input(a):
	"""Processes input and adds both a help system for commands and commands themselves"""
	try:
		command, arg = a[0].split(' ', 1)
	except ValueError:
		command, arg = (a[0], "")
	if not command:
		return None
	elif 'help'.startswith(command) or command.startswith('?'):
		return helper(command, arg)
	else:
		f = command_search(command)
		if f:f(arg)
		else:print(default)

def helper(command, arg):
	"""Searches the command list for the command and trys to read the docstring. if there is no docstring, then it says that there is no info about that command"""
	if "?" in command and command[1:]:
		arg = command[1:]
	if arg and not "help".startswith(arg):
		f = command_search(arg)
		if f:printer(f.__doc__)
		else:printer(no_help)
	else:
		printer(default_help)
	return True


def command_search(command):
	"""Searches the dictionaries of commands for an added command and returns it, otherwise it returns None"""
	for d in commands.commands:
		for k in d:
			if k.startswith(command):
				return d[k]
