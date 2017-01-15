import sys
import states
try:
	import Queue as queue
except ImportError:
	import queue

event_queue = queue.Queue()
global_event_handlers = {'on_start': [], 'on_quit': [], 'on_input': [], 'on_exit': [], 'on_tick': [], 'on_keydown': []}
screens = {'global_event_handlers': global_event_handlers}

class Event(object):
	def __init__(self, type, screen=None, value=[]):
		self.type = type
		self.screen = screen
		self.value = value

def tasks():
	"""Runs through python's thread safe queue. It only takes function calls to get and add event_queue, so there is no way to do it on a 4 loop unless we do a range for loop. The while loop is what they use in the python example, so that is what is used here. In each event return None to let tasks pass to the next level in the event's handler, True to stop the processing of handlers and False to quit the window."""
	while event_queue.qsize() and states.running:
		try:
			t = event_queue.get_nowait()
			r = process(t)
			if r == False:
				quit()
			#This next line is for the user input thread loop to know when it can except user input
			if states.input_type == "prompt":states.input_time = True
			event_queue.task_done()
		except queue.Empty:
			break

def quit():
	"""Does everything for a gentle quit"""
	trigger('on_quit')
	@add
	def on_quit(a):
		states.running = False

def process(event):
	"""The function that runs all event_queue. If an event returns True it breaks, if it returns False it returns False so the program can quit. The processing of event_handlers is from end to start, so earlier handlers are processed after newer handlers. It cycles through screens from first to last though."""
	if event.screen:
		screen = screens.get(event.screen, {})
		r = run_events(screen, event)
		if r == False:return False
	for screen in screens.values():
		r = run_events(screen, event)
		if r == False:return False

def run_events(screen, event):
	"""runs the different event handlers inside one event type"""
	handlers = screen.get(event.type, [])
	for h in reversed(handlers):
		r = h(event.value)
		if r:
			break
		elif r == False:
			return False

def add_screen(name, screen):
	"""Pass a dict in and it will be added to the end of the screens list so it can be processed"""
	screens[name] = screen

def remove_screen(name):
	"""Pass the name of the dict you wish to remove"""
	del(screens[name])

def add(type, func=None, screen="global_event_handlers"):
	"""One can pass either a function named with the name of the event they would like to handle, or they can pass the event handler name like 'on_input' then the function. Beware that some functions may have arguments. 'on_input' has an argument of the input for example."""
	if not screens.get(screen):screens[screen] = {}
	if hasattr(type, '__call__'):
		if screens[screen].get(type.__name__):
			screens[screen][type.__name__].append(type)
		else:
			screens[screen][type.__name__] = [type,]
	elif isinstance(type, str) and not func:
		screen = type
		if not screens.get(screen):screens[screen] = {}
		def adder_function(f):
			if screens[screen].get(f.__name__):screens[screen][f.__name__].append(f)
			else:screens[screen][f.__name__] = [f]
			return f
		return adder_function
	else:
		if screens[screen].get(type):
			screens[screen][type].append(func)
		else:
			screens[screen][type] = [func,]

def remove(type, screen='global_event_handlers'):
	"""Pass the name of the event to remove the latest handler"""
	if screens.get(screen):
		if screens[screen].get(type):
			screens[screen][type].pop()

def trigger(event, args=[], screen=None):
	"""Give the event type as a string and it will happen on the event queue. If a screen is specified it will only trigger the event on that one screen."""
	event_queue.put(Event(event, screen, args))


class Screen(object):
	"""Creates a class where one can add_screen() and it will add the screen in this class to the screens list, add, add a handler to the screen and the related removal functions"""
	def __init__(self, name, default_dict={}, **kwargs):
		default_dict.update(kwargs)
		self.screen = default_dict
		self.name = name

	def add(self, type, func=None):
		"""One can pass either a function named with the name of the event they would like to handle, or they can pass the event handler name like 'on_input' then the function. Beware that some functions may have arguments. 'on_input' has an argument of the input for example. The screen will add the event to the spacific screen"""
		if hasattr(type, '__call__'):
			if self.screen.get(type.__name__):
				self.screen[type.__name__].append(type)
			else:
				self.screen[type.__name__] = [type,]
		else:
			if self.screen.get(type):
				self.screen[type].append(func)
			else:
				self.screen[type] = [func,]

	def add_functions(self, event_type, function_list):
		"""Pass in a list of events and they will be added to the current event queue with the event_type as their event type"""
		function_list = list(function_list)
		if self.screen.get(event_type):
			self.screen[event_type] += function_list
		else:
			self.screen[event_type] = function_list

	def remove(self, type):
		"""Pass the name of the event to remove the latest handler"""
		self.screen[type].pop()

	def add_screen(self):
		"""Adds the screen to the screens list"""
		screens[self.name] = self.screen

	def remove_screen(self):
		"""Removes the screen from screens"""
		del(screens[self.name])
