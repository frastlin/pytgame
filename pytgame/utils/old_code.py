
def user_input2():
	"""We are treating cmdloop like a raw_input with a processor. When states.input_time == False it won't trigger"""
	while states.running:
		if states.input_time:
			app_cmd.cmdloop()
			states.input_time = False
		else:
			time.sleep(fps)

def user_input1():
	"""This runs on a seperate thread from the game loop because otherwise the loop would pause waiting for the user's input. Because it gets anoying to see > before the text and not on the bottom, when most text is passed to the screen, this while loop is told to wait untill the text has been rendered before asking the user for data. Currently the only way to deal with this for schedule event_queue is to use a printer function that prints >."""
	while states.running:
		if states.input_time:
			events.trigger('on_input', [raw_input(">"),])
			states.input_time = False
		else:
			time.sleep(fps)
	print("leaving user_input")


