#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

class SegmentDisplay(object):


	DIO = 13
	CLK = 12
	STB = 11

	LSBFIRST = 0
	MSBFIRST = 1


	def _shiftOut(self, dataPin, clockPin, bitOrder, val):
		for i in range(8):
			if bitOrder == self.LSBFIRST:
				GPIO.output(dataPin, val & (1 << i))
			else:
				GPIO.output(dataPin, val & (1 << (7 -i)))
			GPIO.output(clockPin, True)
			time.sleep(0.000001)			
			GPIO.output(clockPin, False)
			time.sleep(0.000001)			
		
	def sendCommand(self, cmd):
		GPIO.output(self.STB, False)
		self._shiftOut(self.DIO, self.CLK, self.LSBFIRST, cmd)
		GPIO.output(self.STB, True)

	def TM1638_init(self):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.DIO, GPIO.OUT)
		GPIO.setup(self.CLK, GPIO.OUT)
		GPIO.setup(self.STB, GPIO.OUT)
		self.sendCommand(0x8f)

	def numberDisplay(self, num):
		digits = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f]
		self.sendCommand(0x40)
		GPIO.output(self.STB, False)
		self._shiftOut(self.DIO, self.CLK, self.LSBFIRST, 0xc0)
		self._shiftOut(self.DIO, self.CLK, self.LSBFIRST, digits[num/1000%10])
		self._shiftOut(self.DIO, self.CLK, self.LSBFIRST, 0x00)
		self._shiftOut(self.DIO, self.CLK, self.LSBFIRST, digits[num/100%10])
		self._shiftOut(self.DIO, self.CLK, self.LSBFIRST, 0x00)
		self._shiftOut(self.DIO, self.CLK, self.LSBFIRST, digits[num/10%10])
		self._shiftOut(self.DIO, self.CLK, self.LSBFIRST, 0x00)
		self._shiftOut(self.DIO, self.CLK, self.LSBFIRST, digits[num%10])
		self._shiftOut(self.DIO, self.CLK, self.LSBFIRST, 0x00)
		GPIO.output(self.STB, True)

	def numberDisplay_dec(self, num):
		digits = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f]
		integer = 0
		decimal = 0

		pro = int(num * 100)

		integer = int(pro / 100)
		decimal = int(pro % 100)

		self.sendCommand(0x40)
		GPIO.output(self.STB, False)
		self._shiftOut(self.DIO, self.CLK, self.LSBFIRST, 0xc0)
		self._shiftOut(self.DIO, self.CLK, self.LSBFIRST, digits[integer/10])
		self._shiftOut(self.DIO, self.CLK, self.LSBFIRST, 0x00)
		self._shiftOut(self.DIO, self.CLK, self.LSBFIRST, digits[integer%10] | 0x80)
		self._shiftOut(self.DIO, self.CLK, self.LSBFIRST, 0x00)
		self._shiftOut(self.DIO, self.CLK, self.LSBFIRST, digits[decimal/10])
		self._shiftOut(self.DIO, self.CLK, self.LSBFIRST, 0x00)
		self._shiftOut(self.DIO, self.CLK, self.LSBFIRST, digits[decimal%10])
		self._shiftOut(self.DIO, self.CLK, self.LSBFIRST, 0x00)
		GPIO.output(self.STB, True)

	def cleanup(self):
		GPIO.cleanup()


tmp = 0

display = SegmentDisplay()
try:
	display.TM1638_init()
	print("displaying")
	display.numberDisplay(1234)
	time.sleep(4) # 4s
	display.numberDisplay_dec(56.78)
	time.sleep(4) # 4s
	while False:
		display.numberDisplay(tmp)
		tmp += 1
		if tmp > 9999:
			tmp = 0
		time.sleep(0.05)
	
except KeyboardInterrupt:
	display.cleanup()
