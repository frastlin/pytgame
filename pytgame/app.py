import time, threading
try:
	import Queue
except ImportError:
	import queue
from readchar import readkey
import ticker, states, commandline

app_cmd = commandline.App_cmd

fps = 0.05
events = Queue.Queue()
scheduler = ticker.Scheduler()
event_handlers = {'on_start': [], 'on_quit': [], 'on_input': [], 'on_exit': [], 'on_tick': [], 'on_keydown': []}

class Event(object):
	def __init__(self, type, value=[]):
		self.type = type
		self.value = value

def tasks():
	"""Runs through python's thread safe queue. It only takes function calls to get and add events, so there is no way to do it on a 4 loop unless we do a range for loop. The while loop is what they use in the python example, so that is what is used here. In each event return None to let tasks pass to the next level in the event's handler, True to stop the processing of handlers and False to quit the window."""
	while True:
		try:
			t = events.get_nowait()
			r = process(t)
			if r == False:
				quit()
			if states.input_type == "prompt":states.input_time = True
			events.task_done()
		except Queue.Empty:
			break

def user_input():
	app_cmd.cmdloop()

def user_input1():
	"""This runs on a seperate thread from the game loop because otherwise the loop would pause waiting for the user's input. Because it gets anoying to see > before the text and not on the bottom, when most text is passed to the screen, this while loop is told to wait untill the text has been rendered before asking the user for data. Currently the only way to deal with this for schedule events is to use a printer function that prints >."""
	while states.running:
		if states.input_time:
			trigger('on_input', [raw_input(">"),])
			states.input_time = False
		else:
			time.sleep(fps)

def keydown():
	"""Checks if the user pressed a key or a combo of keys and if so, returns them."""
	k = readkey()
	if k:trigger('on_keydown', [k])

def change_input(prompt=None, keypress=None):
	"""Toggles between raw_input and grabbing chars. The two options are prompt and keypress"""
	input_type = "prompt"
	if keypress or states.input_type == "prompt":
		states.input_time = False
		states.input_type = "keypress"
	else:
		states.input_type = "prompt"

def run():
	"""Call this when ever you wish to start the application. In the start the event on_start is created and the typing prompt is called. If you wish text to go before the typing prompt, add it to on_start. This is the main loop of the application."""
	trigger('on_start')
	@add
	def on_start(a):states.input_time = True
	t = threading.Thread(target=user_input)
	t.start()
	while states.running:
		if states.input_type == "keypress":keydown()
		trigger('on_tick')
		tasks()
		scheduler.tick(fps)
		time.sleep(fps)


def quit():
	"""Call this rather than making states.running False. It will take cair of everything. This function is called when an event returns False."""
	trigger('on_quit')
	@add
	def on_quit():
		states.running = False

def process(event):
	"""The function that runs all events. If an event returns True it breaks, if it returns False it returns False so the program can quit. The processing of event_handlers is from end to start, so earlier handlers are processed after newer handlers."""
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
	events.put(Event(event, args))

if __name__ == '__main__':
	def printer(t):print("\n"+t+"\n>")
	scheduler.schedule(printer, delay=1, args=['Hello world!',])
	@add
	def on_input(t):
		if t == "f":
			print("It's f!!!")
		elif t == "quit":
			return False

	@add
	def on_input(t):
		if t == "f":
			print("This is the new f!")
			return True
		elif t == 'p':
			remove('on_input')
			print("Removing...")
		elif t == 'k':
			trigger('on_k')

	@add
	def on_k():
		print("It's a k")


	print("Starting")
	run()

