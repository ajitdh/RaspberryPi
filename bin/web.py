#! /usr/bin/env python3
#  -*- coding:utf-8 -*-

import cherrypy
from bin import webtpl, conf, db
import importlib
import datetime

class Web:
	def __init__(self):
		self.pagina = webtpl.WebTpl()
		
	@cherrypy.expose
	def index(self):
		#version1
		#return '<h1><small>Hallo from</small> meetstation</h1>'
		
		wbMenu = WebMenu()
		self.pagina.setInhoud(wbMenu.menu())
		return self.pagina.genereer()	
	
	@cherrypy.expose
	def over(self):
		wbMenu = WebOver()
		self.pagina.setInhoud(wbMenu.inhoud())
		return self.pagina.genereer()	
		
	def _dht11_temp(self):
		print("-----------------------------------------------")
		
		wm = WebMeting()
		rslt = wm.laatsteMeting()
		rowid = rslt['rowid']
		datum = rslt['datum']
		tijdstip = rslt['tijdstip']
		
		print("RowId1")
		print(rowid)
		
		klasse = '.'.join(['sensor', 'dht11', 'webTemp'])
		mod = importlib.import_module(klasse)
		klasse = getattr(mod, 'Web')
		instantie = klasse()
		resultaat = instantie.meet(rowid)		
		temp = resultaat['meting']
		tmin = '%0.01f &deg;C' % float(resultaat['min'])
		tmax = '%0.01f &deg;C' % float(resultaat['max'])
		tgem = '%0.01f &deg;C' % float(resultaat['gem'])
		
		return {'datum' : datum, 'tijdstip' : tijdstip, 
				'meting' : temp, 'min' : tmin, 'max' : tmax, 'gem' : tgem}
		
		
	@cherrypy.expose
	def dht11_temp(self):
		rslt = self._dht11_temp()
		
		wb = WebWeergave()
		self.pagina.setSensor('dht_temp_js')
		self.pagina.setInhoud(wb.inhoud(datum=rslt['datum'],
										tijdstip = rslt['tijdstip'],
										schaalmin = -20,
										schaalmax = 50,
										titel = 'Temperature',
										label = '°C',
										meting = rslt['meting'],
										min = rslt['min'],
										max = rslt['max'],
										gem = rslt['gem']))
		return self.pagina.genereer()	
		
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def dht11_temp_js(self):
		pass
		
class WebOver:
	def inhoud(self):
		html = '''
		<h1>Meetstation</h1>
		<div id="paginaInhoud" class="linksUitlijnen">
		<p>Python project met Raspberry Pi</p>
		<p>Project </p>
		<p>Sensoren:</p>
		<ul>
			<li>DHT11: temperatuur / relatieve luchtvochtigheid</li>
			<li>BH1750: hoeveelheid licht in lux</li>
			<li>BMP180: luchtdruk in hPa</li>
		</ul>
		</div>
		'''
		
		return html	


class WebMenu:
	def __init__(self):
		self.__lijst = []
		items = str(conf.Conf.get('webinterface','items')).split(',')
		for item in items:
			lijstItem = str(conf.Conf.get('webinterface', item.strip()))
			self.__lijst.append(lijstItem)
	
	def menu(self):
		html  = '<ul data-role="listview" data-inset="true">'
		for item in self.__lijst:
			item = item.split(',')
			html += '''
				<li>
					<a href="%s" class="ui-btn" rel="external">
						<img src="static/afbeeldingen/%s" class="ui-li-thumb">
						<h2>%s</h2>
						<p>%s</p>
					</a>
				</li>
			''' % (item[0].strip(), item[1].strip(), item[2].strip(), item[3].strip())
		
		html = html.replace('__url__',conf.Conf.get('web','serverurl'))
		
		return html
		
	def menuKlein(self):
		html  = '<ul data-role="listview" data-inset="true">'
		for item in self.__lijst:
			item = item.split(',')
			html += '''
				<li>
					<a href="%s" class="ui-btn" rel="external">
						<img src="static/afbeeldingen/%s" class="ui-li-icon"> %s
					</a>
				</li>
			''' % (item[0].strip(), item[1].strip(), item[2].strip())
		
		html = html.replace('__url__',conf.Conf.get('web','serverurl'))
		
		return html
		

class WebMeting:
	def laatsteMeting(self):
		dbSql = "SELECT rowid, jaar, maand, dag, tijdstip FROM meting ORDER BY tijdstip DESC LIMIT 1"
		db.Db.curs().execute(dbSql)
		dbRij = db.Db.curs().fetchone()
		
		maanden = ['januari','februari','maart','april','mei','juni','juli','augustus','september','oktober','november','december']
		datum = '%s %s %s' % (dbRij[3], maanden[int(dbRij[2])], dbRij[1])
		tijdstip = dbRij[4].split(' ')[1]		
		return {'rowid': dbRij[0],
				'datum': datum,
				'tijdstip': tijdstip}
				
class WebWeergave:
	def inhoud(self, **kwargs):
		webmenu = WebMenu().menuKlein()		 
		return '''
		    <h3 id="klok">%s</h3>
		    <h4 d="tijdstip">%s</h4>
			<div id="schaal"></div>
	        <div class="meting">
	                <h4><small>min </small><span id="min">%s</span><br>
	                     <small>max </small><span id="max">%s</span><br>
	                     <small>gem </small><psna id="gem">%s</span></h4>
	        </div>
			<script>
				var schaal = new JustGage({
					id: 'schaal',
					value: %s,
					min: %s,
					max: %s,
					title: '%s',
					label: '%s'
				});
			</script>
	        %s
	        ''' % (kwargs['datum'],kwargs['tijdstip'],kwargs['min'],kwargs['max'],kwargs['gem'],kwargs['meting'],kwargs['schaalmin'],kwargs['schaalmax'],kwargs['titel'],kwargs['label'],webmenu)
