
#! /usr/bin/env/ python3
# -*- coding:utf-8-*-

#meetstation > meet.py

# TEST1
#import bin.conf as conf
#print(conf.Conf.get('sensor', 'licht'))

# TEST2
#import bin.db as db
#db.Db.curs()

from bin import meet
from bin import dbsetup
import os

if __name__ == '__main__':	
	os.chdir(os.path.dirname(os.path.realpath(__file__)))
	meet.Meet()
	
