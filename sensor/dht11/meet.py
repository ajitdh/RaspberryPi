#! /usr/bin/env/ python3
# -*- coding:utf-8-*-

#meetstation > sensor > dht11 > meet.py

from multiprocessing import Process, Manager
import os
import subprocess
import time
from bin import db, conf
import logging

logObj = logging.getLogger('__logger__')

class Meet:
	def __init__(self, rowid=0, args=[]):
		self.logObj = logging.getLogger('meetlog')
		self.rowid = rowid;
		self.poort = args[0];		
		self.timeout = float(conf.Conf.get('sensor', 'timeout'));
		self.pogingen = int(conf.Conf.get('sensor', 'pogingen'));
		self.logObj.debug('DHT11 initieren voltooid') 		
		
	def logMeting(self):		
		manager = Manager()
		self.meting = manager.dict()
		self.meting['succes'] = False
		self.meting['temp'] = 0
		self.meting['relvocht'] = 0
		tel = 1
		while True:
			p = Process(target=self.meet, args=(self.meting,))
			p.start()
			time.sleep(self.timeout)
			if p.is_alive():
				p.terminate()
			if self.meting['succes']:
				self.registreer()
				self.logObj.debug('DHT11 poging %i geslaagd' %tel)
				break
			tel += 1
			if tel > self.pogingen:
				self.logObj.debug('DHT11 meting gefaald')
				break
			
	
	def meet(self, meting):
		pad = os.path.join(os.getcwd(), 'sensor', 'dht11', 'dht')#/home/pi/Projecten/meetstation/sensor/dht11/dht
		rslt = subprocess.check_output([pad, self.poort]).decode('utf-8').strip().split(',')
		if len(rslt) == 2:
			meting['succes'] = True
			meting['relvocht'] = rslt[0]
			meting['temp'] = rslt[1]
			self.logObj.debug('DHT11 relvocht %s, temp %s' % (rslt[0], rslt[1]))
		
	def registreer(self): 
		dbSql = "INSERT INTO dht11 (rowid,temp,relvocht) VALUES (?,?,?)"
		db.Db.curs().execute(dbSql, (self.rowid, self.meting['temp'],self.meting['relvocht']))
		db.Db.conn().commit()
		self.logObj.debug('DHT11 rij succesvol aan tabel toegevoegd')
		
