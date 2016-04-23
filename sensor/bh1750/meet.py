#! /usr/bin/env/ python3
# -*- coding:utf-8-*-

#meetstation > sensor > bh1750 > meet.py

from bin import conf, db
import logging
import threading
import time
import sensor.bh1750.bh1750 as bh1750

class Meet:
	def __init__(self, rowid=0, args=[]):
		self.logObj = logging.getLogger('meetlog')
		self.rowid = rowid
		self.resolutie = args[0]
		self.timeout = int(conf.Conf.get('sensor','timeout'))
		self.pogingen = int(conf.Conf.get('sensor','pogingen'))
		self.logObj.debug('BH1750 initieren voltooid')
		
	def logMeting(self):
		self.meting = { 'succes': False,
						'licht': 0}
		tel = 1
		while True:
			t = threading.Thread(target = self.meet)
			t.daemon = True
			t.start()
			t.join(self.timeout)
			time.sleep(self.timeout)
			if(t.is_alive):
				t._stop()
			
			if self.meting['succes']:
				self.logObj.debug('BH1750 poging % geregistreerd' % tel)
				self.registreer();
				break;
			
			tel += 1
			if tel > self.pogingen:
				self.logObj.debug('BH1750 meting gefaald')
				break
	
	def meet(self):
		bh = bh1750.BH1750()
		self.meting['licht'] = bh.meet(self.resolutie)
		self.meting['succes'] = True
		self.logObj.debug('BH1750 meet succesvol voltooid')
	
	def registreer(self):
		dbSql = "INSERT INTO bh1750 (rowid,licht) VALUES (?,?)"
		db.Db.curs().execute(dbSql, (self.rowid, self.meting['licht']))
		db.Db.conn().commit()
		self.logObj.debug('BH1750 rij succesvol aan tabel toegevoegd')
