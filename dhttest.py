#! /usr/bin/env/ python3
# -*- coding:utf-8-*-

#meetstation > dhttest.py

import subprocess
from threading import Thread
import time
from pcd8544 import driver
import sqlite3
import datetime

lcd = driver.PCD8544()
lcd.led(1)

#lcd.tekst(1, 'HALLO from pi')
#time.sleep(3)
#lcd.led(0)

dbConn = sqlite3.connect('app/meetstation.db')
dbCurs = dbConn.cursor()
dbSql = '''
			CREATE TABLE IF NOT EXISTS tijd	(
			tijd	TEXT, 
			jaar	TEXT, 
			maand	TEXT, 
			dag		TEXT)
		'''
dbCurs.execute(dbSql)

dbSql = '''
			CREATE TABLE IF NOT EXISTS dht11(
			temp	REAL, 
			relvocht REAL)
		'''		
dbCurs.execute(dbSql)
dbCurs.close()
dbConn.close()

def registreer(temp, relvocht):	
	dbConn = sqlite3.connect('app/meetstation.db')
	dbCurs = dbConn.cursor()
	
	tijdstip = str(datetime.datetime.now()).split('.')[0]
	tmp = tijdstip.split(' ')[0].split('-')
	jaar = tmp[0]
	maand = tmp[1]
	dag = tmp[2]

	#lets insert time
	dbSql = '''
			INSERT INTO tijd(tijd,jaar,maand,dag) VALUES(?,?,?,?)
			'''
	dbCurs.execute(dbSql, (tijdstip, jaar, maand, dag))
	rowid = dbCurs.lastrowid
	dbConn.commit()
	
	#lets insert temp and relvocht data
	dbSql = '''
			INSERT INTO dht11(rowid,temp,relvocht) VALUES(?,?,?)
			'''
	dbCurs.execute(dbSql, (rowid, temp, relvocht))	
	dbConn.commit()
	
	#lets select and print data
	dbSql = '''
			SELECT MAX(temp), MIN(temp), MAX (relvocht), MIN(relvocht), AVG(temp), AVG(relvocht)
			FROM dht11
			WHERE rowid IN (SELECT rowid FROM tijd where jaar=? AND maand=? AND dag=?)
			'''
	dbCurs.execute(dbSql,(jaar,maand,dag))		
	rij = dbCurs.fetchone()
	print(rij)
	rij = str(rij)
	rij = rij.split(',')
	
	lcd.tekst(0,('MAXtemp :%s°C'%rij[0].split('(')[1]).center(16))
	lcd.tekst(1,('MINtemp :%s°C'%rij[1]).center(16))
	lcd.tekst(2,('MAXvocht:%s%%'%rij[2]).center(16))
	lcd.tekst(3,('MINvocht:%s%%'%rij[3]).center(16))
	lcd.tekst(4,('MINvocht:%s%%'%rij[4]).center(16))
	lcd.tekst(5,('MINvocht:%s%%'%rij[5].split(')')[0]).center(16))
		
	dbCurs.close()
	dbConn.close()
	
def meet():	
	meeting = subprocess.check_output(['./sensor/dht','5'])		
	meeting = meeting.decode('utf-8').strip().split(',')	
	if len(meeting)==2:
		temp = meeting[1]
		relvocht = meeting[0]		
		
		#lcd.tekst(0,('temp	  : %s°C'%temp).center(16))		
		#lcd.tekst(3,('vochtigh: %s%%'%relvocht).center(16))
		
		registreer(temp, relvocht)	

while True:
	try:
		t = Thread(target=meet)
		t.daemon = True
		t.start()
		t.join(1)
		time.sleep(5)
	except KeyboardInterrupt:
		lcd.led(0)
		break
