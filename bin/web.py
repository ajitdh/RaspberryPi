#! /usr/bin/env/ python3
# -*- coding:utf-8-*-

# > bin > web.py

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
		
class WebMenu:
	def __init__(self):
		self._lijst = []
		items = str(conf.Conf.get('webinterface', 'items')).split(',')
		for item in items:
			lijstItem = str(conf.Conf.get('webinterface', item.strip()))
			self._lijst.append(lijstItem)
	
	def menu(self):
		html = '<ul data-role="listview" data-inset="true">'
		for item in _lijst:
			item = item.split(',')
			html += '''
			<li>
				<a href="%s" class="ui-btn" rel="external">
					<img src="static/afbeeldingen/%s" class="ui-li-thumb">
					<h2>%s<h2>
					<p>%s<p>
				</a>
			</li>
			''' % (item[0].strip(), item[1].strip(), item[2].strip(), item[3].strip())
		html += '</ul>'
		
		#--todo

		return html
