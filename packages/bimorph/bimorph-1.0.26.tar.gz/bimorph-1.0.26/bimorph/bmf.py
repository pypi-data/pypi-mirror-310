def hello(name):
	print("Привет тебе " +name +"!")

def run(name):
	print("Запуск ./bmf sqlite://tmp.sqlite" ,__dir__)

	#import os
	#print(os.system('./bmf sqlite://test.sqlite'))

	import subprocess
	#print(subprocess.check_output(['./bmf', 'sqlite://tmp.sqlite']))
	print(subprocess.check_output(['ls', '-l']))

	#import subprocess
	#subprocess.call(["./bmf sqlite://test.sqlite"])
	#process = subprocess.run(['ls', '-l', '-a'])

