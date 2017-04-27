import cherrypy
from causeweb import config
from causeweb.site.config import ConfigSite
from causeweb.logs import Logs


Logs()

def run_server():
	""" Start the application
	"""
	site_config = ConfigSite({
		'tools.response_headers.on': True,
		'tools.response_headers.headers': [
			('Access-Control-Allow-Origin', '*'),
			('Access-Control-Allow-Headers', 'Authorization'),
			('Content-Type', 'text/json, text/html'),
			('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, PATCH'),
		],
	})

	site_config.add_folder('data/pdfs')
	site_config.add_config({
		'/downloads': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': 'data/pdfs'
		}
	})

	site_config.add_page('Api', config.WEBROOT)
	site_config.complete()


def application(environ, start_response):
	""" Run the web application with UWSGI
	"""
	run_server()
	return cherrypy.tree(environ, start_response)

""" Run the web application without UWSGI
"""
if __name__ == '__main__':
	cherrypy.config.update({
		'server.socket_port': 80
	})

	run_server()
	cherrypy.engine.start()
