import sys

class DateFormatException(Exception) :

	def __init__(self,msg) :
		self.msg=msg

	def __str__(self) :
		return self.msg


class LocationFormatException(Exception) :

	def __init__(self,msg) :
		self.msg=msg

	def __str__(self) :
		return self.msg


class SeleniumDriverException(Exception) :

	def __init__(self,msg) :
		self.msg=msg

	def __str__(self) :
		return self.msg
		

