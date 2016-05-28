#! /usr/bin/env python3
#  -*- coding:utf-8 -*-
# Projecten/meetstation/sensor/hmc5883l/hmc5883l.py
import smbus
import time
import math

class HMC5883L:
	def __init__(self):
		self._bus = smbus.SMBus(1)
		self._sensor = 0x1E
		
		self._regs = {
			'CONF_A': 0x00,
			'CONF_B': 0x01,
			'MODE'  : 0x02,
			'X'     : 0x03,
			'Y'     : 0x07,
			'Z'     : 0x05,
			'STATUS': 0x09
		}
		
		self._tblVersterking = {
			0.88: [0x00, 0.73],
			1.3 : [0x20, 0.92],
			1.9 : [0x40, 1.22],
			2.5 : [0x60, 1.52],
			4.0 : [0x80, 2.27],
			4.7 : [0xA0, 2.56],
			5.6 : [0xC0, 3.03],
			8.1 : [0xE0, 4.35]
		}
		
		# REGISTER CONF_A
		# gemiddelde aantal metingen
		# bit 6 + 5
		# 0x00 1 meting, 0x20 2 metingen, 0x40 4m, 0x60 8 m
		self._regA_gem = 0x60
		
		# overdracht snelheid
		# bit 4 + 3 + 2
		# 0x00 0.75Hz, 0.04 1.5Hz, 0x08 3Hz, 0x0C 7.7Hz, 
		# 0x10 15Hz, standaard, 0x14 30Hz, 0x18 75Hz
		self._regA_overdracht = 0x10
		
		# meetmode
		# 0x00 standaard, 0x01 positieve bias,
		# 0x02 negatieve bias, 0x03 gereserveerd
		self._regA_meetmode = 0x00
		
		# regster B
		# versterking, zie tabel boven
		# bit 7 + 6 + 5
		self._versterking = 1.3
		self._regB_versterking = self._tblVersterking[self._versterking][0]
		self._regB_schaal = self._tblVersterking[self._versterking][1]
		
		# mode
		# bit 1 + 0
		# 0x00 continu meter, 0x01 enkelvoudig meten
		self._regMode_mode = 0x01
		
	def zetGemMeting(self, aantal=8):
		pass
		
	def zetEnkelvoudigMeten(self):
		pass
	
	def zetContinuMeet(self):
		pass
		
	def zetVersterking(self, versterking=1.3):
		pass
		
	def zetOverdracht(self, snelheid=15):
		pass
		
	def meet(self):
		regA = self._regA_gem + self._regA_overdracht + self._regA_meetmode
		self._bus.write_byte_data(self._sensor,self._regs['CONF_A'], regA)
		
		regB = self._regB_versterking
		self._bus.write_byte_data(self._sensor,self._regs['CONF_B'], regB)
		
		regMode = self._regMode_mode
		self._bus.write_byte_data(self._sensor,self._regs['MODE'], regMode)
		
		return self._verwerk()
		
	def zelftest(self):
		
		self._bus.write_byte_data(self._sensor,self._regs['CONF_A'], 0x71)
		
		
		self._bus.write_byte_data(self._sensor,self._regs['CONF_B'], 0xA0)
		
		
		self._bus.write_byte_data(self._sensor,self._regs['MODE'], 0x00)
		
		return self._verwerk()
		
	def _tweeComplement(self, getal=0):
		if getal > 0x8000:
			getal = -((65535 -getal) +1)
		return getal
		
	def _verwerk(self):
		time.sleep(0.007)
		while self._bus.read_byte_data(self._sensor,self._regs['STATUS']) & 0x01 == 0x00:
			time.sleep(0.00025)
			
		xmsb, xlsb, zmsb, zlsb, ymsb, ylsb = self._bus.read_i2c_block_data(self._sensor, self._regs['X'], 6)
		
		x = self._tweeComplement(256 * xmsb + xlsb)
		x *= self._regB_schaal
		
		y = self._tweeComplement(256 * ymsb + ylsb)
		y *= self._regB_schaal
		
		z = self._tweeComplement(256 * zmsb + zlsb)
		z *= self._regB_schaal
		
		yx = math.atan2(y,x)
		yx = yx + 2*math.pi if yx < 0 else yx
		
		zx = math.atan2(y,x)
		zx = zx + 2*math.pi if zx < 0 else zx
		
		zy = math.atan2(y,x)
		zy = zy + 2*math.pi if zy < 0 else zy
		
		return (yx, zx, zy)
		
# === voor de fun of it ==========
compas = HMC5883L()


try:
	while True:
		hoek = math.degrees(compas.meet()[0])
		print(hoek)
		time.sleep(1)
except KeyboardInterrupt:
	pass
