import sys
import states
try:
	import Queue as queue
except ImportError:
	import queue

event_queue = queue.Queue()
event_handlers = {'on_start': [], 'on_quit': [], 'on_input': [], 'on_exit': [], 'on_tick': [], 'on_keydown': []}

class Event(object):
	def __init__(self, type, value=[]):
		self.type = type
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
	"""The function that runs all event_queue. If an event returns True it breaks, if it returns False it returns False so the program can quit. The processing of event_handlers is from end to start, so earlier handlers are processed after newer handlers."""
	handlers = event_handlers.get(event.type, [])
	for h in reversed(handlers):
		r = h(event.value)
		if r:
			break
		elif r == False:
			return False

def add(type, func=None):
	"""One can pass either a function named with the name of the event they would like to handle, or they can pass the event handler name like 'on_input' then the function. Beware that some functions may have arguments. 'on_input' has an argument of the input for example."""
	if hasattr(type, '__call__'):
		if event_handlers.get(type.__name__):
			event_handlers[type.__name__].append(type)
		else:
			event_handlers[type.__name__] = [type,]
	else:
		if event_handlers.get(type):
			event_handlers[type].append(func)
		else:
			event_handlers[type] = [func,]

def remove(type):
	"""Pass the name of the event to remove the latest handler"""
	event_handlers[type].pop()

def trigger(event, args=[]):
	"""Give the event type as a string and it will happen on the event queue. If there is no entry in event_handlers a new entry will be created with it"""
	if event_handlers.get(event) == None:
		event_handlers[event] = []
	event_queue.put(Event(event, args))

