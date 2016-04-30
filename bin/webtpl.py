#! /usr/bin/env/ python3
# -*- coding:utf-8-*-

# > bin > webtpl.py

from bin import conf

class WebTpl:
	def __init__(self):		
		#inhoud -> content
		#weergave -> reproduction		
		servertitle = conf.Conf.get('web', 'servertitel')
		
		self.weergave = {'head' : '',
						 'titel' : servertitle,
						 'inhoud' : ''}
						 
		self.docHead = [['title',servertitle],
						['js', 	'jquery.js'],
						['css', 'jqm/jquery.mobile-1.4.5.min.css'],
						['js', 	'jqm/jquery.mobile-1.4.5.min.js'],
						['js', 	'justgage/justgage-1.2.2/raphael-2.1.4.min.js'],
						['js', 	'justgage/justgage-1.2.2/justgage.js'],						
						['css', 'layout/meetstation.css'],
						['js',  'layout/meetstation.js']]
	
	#method responsible to 
	def genereer(self):
		self._prepHead();
		return self._tpl();
		
	def setInhoud(self, inhoud=''):
		self.weergave['inhoud'] = inhoud

	def _prepHead(self):
		html = ''
		
		for item in self.docHead:
			type = item[0]
			bron = item[1]
			
			if(type == 'title'):
				html += '<title>%s</title>' %bron
				self.weergave['titel']
			elif(type == 'js'):
				html += '<script src="static/%s"></script>' %bron
			else:
				html += '<link rel="stylesheet" href="static/%s"/>' %bron
		
		self.weergave['head'] = html		
		
	def _tpl(self):
		#return 'Hello from PI in the sky'
		
		html = '''
		<!DOCTYPE>
		<html>
			<head>%s</head>
			<body>
				<div data-role="page">
					<header data-role="header" data-position="fixed">
						<h1>%s</h1>
						<div data-role="navbar">
							<ul>
								<li><a href="/" class="ui-btn" data-icon="home">Home</a></li>
								<li><a href="/over" class="ui-btn" data-icon="info">Over</a></li>
							</ul>
						</div>
					</header>
					<section class="ui-content" id="inhoud">
						%s
					</section>
					<footer data-role="footer" data-position="fixed">
						<h4>copyright &copy; %s </h4>
					</footer>
				</div>
			</body>
		</html>
		''' % (self.weergave['head'], self.weergave['titel'], self.weergave['inhoud'], self.weergave['titel'])
		
		return html
