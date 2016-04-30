#! /usr/bin/env/ python3
# -*- coding:utf-8-*-

# meetstation > web.py

from bin import web, webtpl, conf
import cherrypy
import os
import subprocess

if __name__ == '__main__':
	
	iplijst = subprocess.check_output(['hostname', '-I']).decode('utf-8').split(' ')	
	if len(iplijst) > 0:
		serveradres = iplijst[0]
		print(serveradres)
		
		cherrypy.config.update({
			'server.socket_host' : serveradres,
			'server.socket_port' : 80
		})
		
		conf = {'/': {
					'tools.sessions.on': True,
					'tools.staticdir.root': os.path.abspath(os.getcwd())
				},
				'/static': {
					'tools.staticdir.on': True,
					'tools.staticdir.dir': 'public'
				},
			}
	
		try:
			print('lets try')
			cherrypy.quickstart(web.Web(), '/', conf)
			cherrypy.engine.start()
		except:
			print ("Unexpected error:", sys.exc_info()[0])
			
		
