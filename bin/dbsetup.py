#! /usr/bin/env/ python3
# -*- coding:utf-8-*-

#meetstation > bin > dbsetup.py

from bin import db
import logging
from bin import logger

class Setup:	
	def __init__(self):
		logger.Logger('dblog') # calls the constructor
		self.logObj = logging.getLogger('dblog') #dblog = db
		self._meeting()
		self._dht11()
		self._bh1750()
		
	def _meeting(self):
		try:
			dbSql = "DROP TABLE IF EXISTS meting"
			db.Db.curs().execute(dbSql)
			
			dbSql = "CREATE TABLE meting" +\
					"(tijdstip TEXT," +\
					" jaar TEXT," +\
					" maand TEXT," +\
					" dag TEXT)"
			db.Db.curs().execute(dbSql)
			
			dbSql = "CREATE UNIQUE INDEX ndxTijdstip ON meting(tijdstip)"
			db.Db.curs().execute(dbSql)
			self.logObj.debug('DBSETUP tabel meting succesvol aangemaakt')
			
		except Exception as e:
			self.logObj.error('DBSETUP _meeting: ' + e.args[0])

	def _dht11(self):
		try:
			dbSql = "DROP TABLE IF EXISTS dht11"
			db.Db.curs().execute(dbSql)
			
			dbSql = "CREATE TABLE dht11" +\
					"(temp INT," +\
					" relvocht INT)"
			db.Db.curs().execute(dbSql)
			self.logObj.debug('DBSETUP tabel dht11 succesvol aangemaakt')
			
		except Exception as e:
			self.logObj.error('DBSETUP _dht11: ' + e.args[0])
			
	def _bh1750(self):
		try:
			dbSql = "DROP TABLE IF EXISTS bh1750"
			db.Db.curs().execute(dbSql)
			
			dbSql = "CREATE TABLE bh1750" +\
					"(licht INT UNSIGNED)"
			db.Db.curs().execute(dbSql)
			self.logObj.debug('DBSETUP tabel bh1750 succesvol aangemaakt')
			
		except Exception as e:
			self.logObj.error('DBSETUP _bh1750: ' + e.args[0])
