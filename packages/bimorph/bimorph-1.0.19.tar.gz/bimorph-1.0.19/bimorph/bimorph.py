def hello(name):
	print("Привет " +name +"!")

def bmf(name):
	print("Запуск ./bmf sqlite://tmp.sqlite")

	import os
	#os.system('./bmf sqlite://test.sqlite')

	import subprocess
	#subprocess.call(["./bmf sqlite://test.sqlite"])
	process = subprocess.run(['ls', '-l', '-a'])

