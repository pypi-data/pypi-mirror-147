# bas.py

class BasInfo:
	'''
	Example:

	my = BasInfo('BAS')
	my.company = 'MIMO Tech'
	my.hobby = ['Play','Reading','Sleeping']
	print(my.name)
	my.show_email()
	my.show_myart()
	my.show_hobby()

	'''
	def __init__(self,name):
		self.name = name
		self.company = ''
		self.hobby = []
		self.art = '''
		      |\\      _,,,---,,_
		ZZZzz /,`.-'`'    -.  ;-;;,_
		     |,4-  ) )-,_. ,\\ (  `'-'
		    '---''(_/--'  `-'\\_)  Miao Miao 
		'''
		self.art2 = '''
		 _._     _,-'""`-._
		(,-.`._,'(       |\\`-/|
		    `-.-' \\ )-`( , o o)
		          `-    \\`_`"'-
		'''
		self.art3 = '''
		   .------\\ /------.
		   |       -       |
		   |               |
		   |               |
		   |               |
		_______________________
		===========.===========
		  / ~~~~~     ~~~~~ \
		 /|     |     |\
		 W   ---  / \\  ---   W
		 \\.      |o o|      ./
		  |                 |
		  \\    #########    /
		   \\  ## ----- ##  /
		    \\##         ##/
		     \\_____v_____/

		'''

	def show_email(self):
		if self.company != '':
			print('{}@{}.com'.format(self.name.lower(),self.company))
		else:
			print('{}@gmail.com'.format(self.name.lower()))

	def show_myart(self):
		print(self.art)

	def show_cat(self):
		print(self.art2)

	def show_loong(self):
		print(self.art3)

	def show_hobby(self):
		if len(self.hobby) !=0:
			print('-------my hobby-------')
			for i,h in enumerate(self.hobby,start=1):
				print(i, h)
			print('----------------------')
		else:
			print('No hobby')


if __name__ == '__main__':
	my = BasInfo('BAS')
	my.company = 'MIMO Tech'
	my.hobby = ['Play','Reading','Sleeping']
	print(my.name)
	my.show_email()
	my.show_myart()
	my.show_hobby()
	my.show_cat()
	my.show_loong()
	# help(my)


