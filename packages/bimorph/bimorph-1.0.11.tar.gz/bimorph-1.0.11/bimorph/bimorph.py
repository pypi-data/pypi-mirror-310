print("bimmorph.py")

import os

def hello(name):
	print("Привет " +name)

def bmf(name):
	print("Запуск ./bmf sqlite://tmp.sqlite")
	os.system('./bmf sqlite://test.sqlite')


