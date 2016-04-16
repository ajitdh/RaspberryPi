#! /usr/bin/env/ python3
# -*- coding:utf-8-*-

# SMBus (System Management Bus) is a subset from the I2C protocol
# When writing a driver for an I2C device try to use the SMBus commands
# if possible (if the device uses only that subset of the I2C protocol)
# as it makes it possible to use the device driver on both SMBus
# adapters and I2C adapters.
import smbus

#Datasheet: http://www.datasheetspdf.com/PDF/BMP180/770150/1
class BMP180:
	def __init__(self):
	
		# 0 = /dev/i2c-0 (port I2C0)
		# 1 = /dev/i2c-1 (port I2C1)
		self._bus = smbus.SMBus(1)
		
		#7 bit address (will be left shifted to add the read write bit)
		self._sensor = 0x77  
		
		self._register = {'CALIB': 0xAA,
						  'MEET': 0xFA,
						  'MSB': 0xF6,
						  'LSB': 0xF7}
						  
		self._calib = {'AC1' : 0,
					   'AC2' : 0,
					   'AC3' : 0,
					   'AC4' : 0,
					   'AC5' : 0,
					   'AC6' : 0,
					   'B1' : 0,
					   'B2' : 0,
					   'MB' : 0,
					   'MC' : 0,
					   'MD' : 0}
		 
		# oversampling 0, 1, 2, of 3
		self._oss = 3
		
		#Control registers values for different internal oversampling_setting (oss)
		# TEMP - Temperature
		# OSS - Pressure
		self._crv = {'TEMP' : 0x2E,
				     '0SS0' : 0x34,
				     '0SS1' : 0x74,
				     '0SS2' : 0xB4,
				     '0SS3' : 0xF4}

		#temperature
		self._temp = 0 		
		
		#pressure
		self._druk = 0
				
	def _signed(self, mb, lb):
		tmp = 256 * mb + lb
		if(tmp > 32767):
			tmp -= 65536
		return tmp
				
	def _unsigned(self, mb, lb):
		return 256 * mb + lb
		
	def meet(self):
		if(self._leesCalib()):
			pass
	
	def _leesCalib(self):
		try:
			calibDta = self._bus.read_i2c_block_data(self._sensor, self._register['CALIB'], 22)
			
			items = [['AC1',True],  # short
				['AC2',True],  # short
				['AC3',True],  # short
				['AC4',False], #unsigned short
				['AC5',False], #unsigned short
				['AC6',False], #unsigned short
				['B1',True],   # short
				['B2',True],   # short 
				['MB',True],   # short
				['MC',True],   # short
				['MD',True]]   # short 
				
			#see page 15 of datasheet
			for ndx, el in enumerate(items):
				pass
			
		except IOError:
			return false
		
bmp =  BMP180()
print (bmp.meet())		
