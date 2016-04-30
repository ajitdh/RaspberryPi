#! /usr/bin/env/ python3
# -*- coding:utf-8-*-

# meetstation > bin > web.py

import cherrypy
from bin import webtpl, conf, db
import importlib

class Web:
	def __init__(self):
		self.pagina = webtpl.WebTpl()
	
	@cherrypy.expose
	def index(self):
		#version1
		#return '<h1><small>Hallo from</small> meetstation</h1>'
		
		return self.pagina.genereer()
