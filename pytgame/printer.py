from textwrap import wrap, TextWrapper
import settings

def printer(text, prompt=False, width=70):
	text = str(text)
	t = text.split('\n')
	final_text = []
	for line in t:
		if line == '':
			final_text += ['',]
		else:
			final_text += wrap(line, width)
	if prompt:final_text += [settings.prompt]
	for i in final_text:
		print(i)

if __name__ == '__main__':
	printer("The world is a funny place frodo baggens,\nfirst the sun rizes,\nthen it sets.\nIt becomes day, then it becomes night. It gets cold and it gets hot. All these things are food for the\n\n\nsoul")
