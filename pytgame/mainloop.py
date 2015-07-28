import time, threading
from readchar import readkey
import user_input, ticker, states, events
from settings import fps

scheduler = ticker.Scheduler()

def keydown():
	"""Checks if the user pressed a key or a combo of keys and if so, returns them."""
	k = readkey()
	if k:events.trigger('on_keydown', [k])

def change_input(prompt=None, keypress=None):
	"""Toggles between raw_input and grabbing chars. The two options are prompt and keypress"""
	input_type = "prompt"
	if keypress or states.input_type == "prompt":
		states.input_time = False
		states.input_type = "keypress"
	else:
		states.input_type = "prompt"

@events.add
def on_quit(a):
	"""Is the default quit method, don't overide this unless states.running is turned to False"""
	states.running = False

def run():
	"""Call this when ever you wish to start the application. In the start the event on_start is created and the typing prompt is called. If you wish text to go before the typing prompt, events.add it to on_start. This is the main loop of the application."""
	events.trigger('on_start')
	@events.add
	def on_start(a):states.input_time = True
	t = threading.Thread(target=user_input.run)
	t.start()
	while states.running:
		if states.input_type == "keypress":keydown()
		events.trigger('on_tick')
		events.tasks()
		scheduler.tick(fps)
		time.sleep(fps)


if __name__ == '__main__':
	@events.add
	def on_quit(a):
		print("goodbye world!")

	@events.add
	def on_take(a):
		print("You took something!")
	run()