from sys import argv
import re

options = {}
args = []

i = 1
while i < len(argv):
	m = re.search("^-([\w-]+)", argv[i])
	if m:
		options[m.group(0)] = True
	else:
		options[m.group(0)] = False

	i += 1

def getOption(name):
	return options[name] if name in options else None
