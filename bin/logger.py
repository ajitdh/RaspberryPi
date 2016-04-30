#! /usr/bin/env/ python3
# -*- coding:utf-8-*-

#meetstation > bin > logger.py

import time
from bin import conf
import logging


class Logger:

    def __init__(self, sleutel):
        cnf = conf.Conf.get('logging')

        logObj = logging.getLogger(sleutel)

        datum = time.strftime('%d_%m_%Y')

        bestand = conf.Conf.pad(
            [cnf['maplog'], '%s_%s.csv' % (cnf[sleutel], datum)])
        logBestand = logging.FileHandler(filename=bestand)
        logFormat = logging.Formatter(
            fmt='%(asctime)s,%(levelname)s,%(message)s',
            datefmt='%H:%M:%S')
        logBestand.setFormatter(logFormat)
        logObj.addHandler(logBestand)

        if cnf['level'] == 'DEBUG':
            logObj.setLevel(logging.DEBUG)
        elif cnf['level'] == 'INFO':
            logObj.setLevel(logging.INFO)
        elif cnf['level'] == 'WARNING':
            logObj.setLevel(logging.WARNING)
        elif cnf['level'] == 'CRITICAL':
            logObj.setLevel(logging.CRITICAL)
        else:
            logObj.setLevel(logging.ERROR)
