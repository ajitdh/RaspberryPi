#! /usr/bin/env/ python3
# -*- coding:utf-8-*-

#meetstation > bin > conf.py

import configparser
import os
import sys

class Conf:
	oConf = None
	
	class __Conf:
		__conf = None
		
		def __init__(self):
			self.pad = Conf.pad(['bin', 'conf.ini'])
			try:
				Conf.__Conf.__conf = configparser.ConfigParser()
				Conf.__Conf.__conf.read(self.pad)
			except:
				sys.exit('FOUT... configuratie gefaald')
	
		def __get(blok='', item=''):
			try:
				blok = Conf.__Conf.__conf[blok]
				if len(item) > 0:
					return blok[item]
				else:
					return blok				
			except:
				return false;
	
	@staticmethod
	def get(blok='', item=''):
		if not Conf.oConf:
			Conf.oConf = Conf.__Conf() #makes instance of that object
		
		return Conf.__Conf.__get(blok, item)
		
	@staticmethod
	def pad(padEln = []):
		return os.path.join(os.getcwd(), os.sep.join(padEln))

