import traceback
import mainloop
import commands
import events
import printer
import settings
import states
from game_object import GameObject, default_object
from mainloop import scheduler
from file_parser import create_data

schedule = scheduler.schedule
add = events.add
trigger = events.trigger
add_screen = events.add_screen
remove_screen = events.remove_screen
Screen = events.Screen
register = commands.register
commands = commands.commands
change_input = mainloop.change_input
printer = printer.printer

def run():
	try:
		mainloop.run()
	except:
		traceback.print_exc()
		states.running = False
