#! /usr/bin/env/ python3
# -*- coding:utf-8-*-

#meetstation > bin > db.py

import sqlite3
import bin.conf as conf
import sys

class Db:
	oDb = None
	
	class __Db:
		__conn = None
		__curs = None
		
		def __init__(self):
			try:
				padDb = conf.Conf.pad([conf.Conf.get('database', 'map'), conf.Conf.get('database', 'db')])
				Db.__Db.__conn = sqlite3.connect(padDb)
				Db.__Db.__curs = Db.__Db.__conn.cursor()			
			except:
				sys.exit('Fout... database')
				
		def __del__(self):
			if Db.__Db.__curs:
				Db.__Db.__curs.close()
				Db.__Db.__curs = None
			if Db.__Db.__conn:
				Db.__Db.__conn.close()
				Db.__Db.__conn = None
		
	@staticmethod
	def curs():
		if not Db.oDb:
			Db.oDb = Db.__Db()
			
		return Db.oDb.__curs

	@staticmethod
	def conn():
		if not Db.oDb:
			Db.oDb = Db.__Db()
			
		return Db.oDb.__conn
