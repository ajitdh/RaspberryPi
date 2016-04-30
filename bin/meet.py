#! /usr/bin/env/ python3
# -*- coding:utf-8-*-

# meetstation > bin > meet.py

from datetime import datetime
from bin import db
from bin import conf
import importlib
from bin import logger
import logging


class Meet:

    def __init__(self):
        self.rowid = None

        logger.Logger('meetlog')
        self.logObj = logging.getLogger('meetlog')

        # self.logObj.debug('start class meet.py')
        # self.logObj.info('wist je al dat het gestart is')
        # self.logObj.warning('check ip')
        # self.logObj.critical('nothing critical')
# self.logObj.error('no errors!')

            self._tijdstip()
        self._sensoren()

    def _tijdstip(self):
        tijdstip = str(datetime.now()).split('.')[0]
        self.logObj.debug('MEET tijdstip %s ' % tijdstip)
        tmp = tijdstip.split(' ')[0].split('-')
        jaar = tmp[0]
        maand = tmp[1]
        dag = tmp[2]

        dbSql = "INSERT INTO meting (tijdstip, jaar, maand, dag) VALUES(?,?,?,?)"
        try:
            db.Db.curs().execute(dbSql, (tijdstip, jaar, maand, dag))
            self.rowid = db.Db.curs().lastrowid
            db.Db.conn().commit()
            self.logObj.debug('MEET rij toegevoed aan tabel')
        except Exception as e:
            self.logObj.error(e.args[0])

    def _sensoren(self):
        sensorMap = conf.Conf.get('sensor', 'map')  # map = sensor
        sensorItems = conf.Conf.get(
            'sensor', 'items').split(',')  # items = temp, licht
        for item in sensorItems:
            sensor = conf.Conf.get('sensor', item.strip()).split(
                ',')  # temp = dht11,5 or licht = bh1750
            klass = '.'.join([sensorMap, sensor[0].lower(), 'meet'])
            self.logObj.debug('MEET klass %s()' % klass)
            mod = importlib.import_module(klass)
            klass_ = getattr(mod, 'Meet')
            sensor.pop(0)
            instantie = klass_(self.rowid, sensor)
            instantie.logMeting()
