#!/usr/bin/python
#
# -------------------------------------------
# binary count on 8 fold relay card by conrad
# copyright (c) 2010 Michael Aschauer
# Licence: GNU GPLv3
# -------------------------------------------

import serial, time, sys

PORT='/dev/ttyS0'


class RelaisCard:
	
	def __init__(self):
		self.port = 0
		self.ser = 0

	def open(self, port):
		self.port = port
		# open serial
		self.ser = serial.Serial(port, 19200, timeout=10,
			parity=serial.PARITY_NONE, rtscts=0)
		if self.ser.isOpen:       
			print "opened serial port", port
			return True
		else:
			print "failed to open", port
			return False		
			
	def init(self):
		self.send(1,1,0)
		print "ignore",
		return self.read_answer()
		       
	def send(self, b1 = 0, b2 = 0 , b3 = 0):
		if b1 == 3:
			print "    %3d  -> " % b3,	
		checksum = b1 ^ b2 ^ b3
		print "send:", b1, b2, b3, checksum,
		self.ser.write(chr(b1) + chr(b2) + chr(b3) + chr(checksum))
		return self.read_answer()
			
	def read_answer(self):
		ret = self.ser.read(4)
		if ret:
			print "(got answer:",
			checksum = ord(ret[0]) ^ ord(ret[1]) ^ ord(ret[2])
			for i in ret:
				print ord(i),	
			if checksum != ord(ret[3]):
				print "error: checksum should be=%i" % checksum
				return False
			print ")" 
			return True
		else:
			print " - got no answer"
			return False

	def countBinary(self, i):
		self.send(3, 1, i)


def main():
	time.sleep(4)
	
	if sys.argv[1:]:
		port = sys.argv[1]
	else:
		port = PORT 
		
	r = RelaisCard();
	if not r.open(port):
		exit()
		
	print "INITIALIZE RELAIS CARD"
	r.init()
	r.init()	
	print "NOW COUNT"
	while True:
		for i in range(0,255):
			r.countBinary(i)
			time.sleep(1)
		time.sleep(10)	
	ser.close()


if __name__ == "__main__":
    main()

