#! /usr/bin/env python3
# -*- coding:utf-8 -*-

'''
	digitale lichtsensor BH1750VFI
	resolutie 1lx - 65535lx
	maximale gevoeligheid: 0.11lx
	1lx = 1lm / m²
'''

import smbus
import time

class BH1750:
	def __init__(self):
		self._bus = smbus.SMBus(1)
		# adres sensor i2c bus
		self._sensor = 0x23
		
		# gevoeligheid
		# standaard 69, waarde tussen 31 en 254
		self._mtreg = 69
		# standaard resolutie (eigen keuze)
		self._resMode = 'SINGLE_LOW_RES'
		# instructieset
		self._modes = {
				'POWER_DOWN':		0x00,
				'POWER_UP':			0x01,
				'RESET':			0x07,
				'CONT_LOW_RES': 	0x13,
				'CONT_HIGH_RES1':	0x10,
				'CONT_HIGH_RES2':	0x11,
				'SINGLE_LOW_RES': 	0x23,
				'SINGLE_HIGH_RES1':	0x20,
				'SINGLE_HIGH_RES2':	0x21,
			}
		self._setMode('POWER_DOWN')
		self.setGevoeligheid(self._mtreg)
	
	def _setMode(self, mode = 'POWER_DOWN'):
		if mode in self._modes.keys():
			self._bus.write_byte(self._sensor, self._modes[mode])
			
	def _reset(self):
		self._setMode('POWER_UP')
		self._setMode('RESET')
		self._setMode('POWER_DOWN')
		
	def setGevoeligheid(self, gevoeligheid=69):
		try:
			gevoeligheid = int(gevoeligheid)
			if (gevoeligheid > 30) and (gevoeligheid <255):
				self._mtreg = gevoeligheid
			else:
				self._mtreg = 69
			
			bt765 = (self._mtreg & 0xE0) >> 5
			bt43210 = self._mtreg & 0x1F
			
			self._setMode('POWER_UP')
			self._bus.write_byte(self._sensor,0x40 + bt765)
			self._bus.write_byte(self._sensor, 0x60)
			self._setMode('POWER_DOWN')
			
			
		except ValueError:
			print('fout gevoeligheid')
			
	def powerDown(self):
		self._setMode('POWER_DOWN')
		
	def powerUp(self):
		self._setMode('POWER_UP')
		
	def meet(self, res='SINGLE_HIGH_RES1'):
		self._reset()
		self._setMode('POWER_UP')
		
		if res in list(self._modes.keys())[2:]:
			self._resMode = res
			
		self._setMode(self._resMode)
		
		wacht = 0.016 if self._modes[self._resMode] & 0x03 == 0x03 else 0.200
		if self._mtreg > 69:
			wacht *= self._mtreg /69
		time.sleep(wacht)
		
		dta = self._bus.read_word_data(self._sensor, self._modes[self._resMode])/1.2
		
		if self._modes[self._resMode] & 0x03 == 0x01:
			dta *= 69/(2*self._mtreg)
		elif self._modes[self._resMode]&0x03 == 0x00:
			dta *= 69/self._mtreg
			
		self._setMode('POWER_DOWN')
		
		return dta
		
#bh = BH1750()
#print('%0.01lx' % bh.meet('SINGLE_HIGH_RES2'))
			
			
			
	
		
