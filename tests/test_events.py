from pytgame import events, states

var1 = 0
var2 = 0

def test_add():
	"""Test that add works with both the decorator and the manual way"""
	@events.add
	def on_change(a):
		"""Changes the var1 using the decorator way of add"""
		global var1
		var1 = 42
	def random_function(a):
		"""Another random function that is for testing the non decorator adding of events.add"""
		global var2
		var2 = 52
	events.add('on_change', random_function)
	#Check that it added the events
	assert len(events.event_handlers['on_change']) == 2

def test_trigger():
	#First trigger an event (on_change for the function above)
	events.trigger('on_trigger')
	#check that only one event was added
	assert events.event_queue.qsize() == 1
	#Get our event back from the event queue
	ev = events.event_queue.get_nowait()
	assert ev.type == 'on_trigger'

def test_remove():
	"""Add and remove an event handler"""
	@events.add
	def on_remove(a):
		pass
	assert len(events.event_handlers['on_remove']) == 1
	#Remove the handler
	events.remove('on_remove')
	#check if the remove worked
	assert len(events.event_handlers['on_remove']) == 0

def test_process():
	"""First add some events so that process can test the different types of return"""
	@events.add
	def on_r(a):
		global var1
		var1 = 42
		return False
	@events.add
	def on_r(a):
		global var1
		var1 = 99
		return True
	#Create an event that can be passed to the process function
	e = events.Event('on_r', [])
	result = events.process(e)
	#Check that it returned None and check that var1 is 99
	assert result == None
	assert var1 == 99
	#Now remove the top one and check that process returns False
	events.remove('on_r')
	result = events.process(e)
	#Check that result is False and var1 is 42
	assert result == False
	assert var1 == 42

def test_quit():
	"""Will make sure the quit function adds a 'on_quit' handler and that there is an 'on_quit' event in the event queue"""
	events.quit()
	assert len(events.event_handlers['on_quit']) == 1
	ev = events.event_queue.get_nowait()
	assert ev.type == 'on_quit'

def test_tasks():
	"""First creates some events, one will return false and then another will change a variable"""
	@events.add
	def on_tasks(a):
		return False
	@events.add
	def on_tasks(a):
		global var1
		var1 = 100
	#trigger an event
	events.trigger('on_tasks')
	#Now run tasks
	events.tasks()
	#Check that states.running == False from the on_quit function and that var1 is 100
	assert states.running == False
	assert var1 == 100
