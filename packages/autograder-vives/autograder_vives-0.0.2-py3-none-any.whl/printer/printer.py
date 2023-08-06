import time
import serial

class Printer:
	#ser = serial.Serial("/dev/ttyACM0", baudrate = 9600, parity=serial.PARITY_NONE, 
	#stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

	def __init__(self, port):
		self.__port = "/dev/tty" + ('%s'%(port))
		self.__ser = serial.Serial('%s'%(self.__port), baudrate = 9600, parity=serial.PARITY_NONE, 
		stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
		print("New printer created")

	def print_text(self, text):
		self.__ser.write(b'%s\n'%(text).encode())
		time.sleep(1)
		readedtext = self.__ser.readline()
		print("Printed following text: \n")
		print(readedtext)


	def set_port(self, port):
		self.__newport = "/dev/tty" + ('%s'%(port))
		self.__ser = serial.Serial('%s'%(self.__newport), baudrate = 9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
		print("Port updated to: %s" %(port))


