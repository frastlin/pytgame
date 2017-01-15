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
	assert len(events.screens['global_event_handlers']['on_change']) == 2
	#now test adding to a spacific screen
	@events.add('current_room')
	def on_spin(a):
		pass
	def on_spin(a):
		pass
	events.add('on_spin', on_spin, screen="current_room")
	assert len(events.screens['current_room']['on_spin']) == 2
	events.remove_screen('current_room')

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
	assert len(events.screens['global_event_handlers']['on_remove']) == 1
	#Remove the handler
	events.remove('on_remove')
	#check if the remove worked
	assert len(events.screens['global_event_handlers']['on_remove']) == 0

def test_add_and_remove_screen():
	"""adds and removes a screen"""
	screen1 = {"on_entry": [], "on_exit": []}
	events.add_screen('screen1', screen1)
	assert len(events.screens) == 2
	#check that we can add handlers and have them show up in the events screen:
	screen1['on_jump'] = []
	assert events.screens['screen1']['on_jump'] == []
	#remove the screen1
	events.remove_screen('screen1')
	assert len(events.screens) == 1

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
	e = events.Event('on_r', "", [])
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

def test_process_screens():
	"""Process works above, but now we are going to add some other screens"""
	def f1(a):
		global var2
		var2 = 1000
		return True
	screen1 = {'change_var': [f1]}
	#add another handler in global_events_handler and make sure that when it returns True it stops iteration of the whole loop
	@events.add
	def change_var(a):
		var2 = 2000
	events.add_screen('screen1', screen1)
	events.process(events.Event("change_var"))
	assert var2 == 1000

def test_quit():
	"""Will make sure the quit function adds an 'on_quit' handler and that there is an 'on_quit' event in the event queue"""
	events.quit()
	assert len(events.screens['global_event_handlers']['on_quit']) == 1
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

def test_Screen_init():
	"""Creates screen with different initial arguments"""
	s1 = events.Screen('s1')
	assert s1.screen == {}
	s2 = events.Screen(name='s2', on_jump=42, on_exit=91)
	assert s2.screen['on_jump'] == 42
	d = {'on_exit': 99, 'on_jump': 66}
	s3 = events.Screen('s3', d)
	assert s3.screen['on_exit'] == 99

def test_Screen_add_and_remove():
	"""Creates and adds the function to a screen, then checks that the handler is there."""
	screen3 = events.Screen('s3')
	#for some reason the screen class has the two keyword arguments given above in the function before, so we clear the screen
	screen3.screen = {}
	#test the add decorator like we intended
	@screen3.add
	def on_fly(a):
		pass
	assert len(screen3.screen) == 1
	screen3.remove('on_fly')
	assert len(screen3.screen['on_fly']) == 0

def test_Screen_add_screen_and_remove_screen():
	"""Test the adding and removing of the screen object from the screens list"""
	d = events.screens['global_event_handlers']
	events.screens = {}
	events.screens['global_event_handlers'] = d
	screen4 = events.Screen('screen4', {"on_turn": [], "on_keydown": []})
	#check that the screens list is 1 long:
	assert len(events.screens) == 1
	screen4.add_screen()
	assert len(events.screens) == 2
	#test removing the screen:
	screen4.remove_screen()
	#check that the events.screens is 1:
	assert len(events.screens) == 1
