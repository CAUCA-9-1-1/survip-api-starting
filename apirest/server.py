import cherrypy
from causepy.logging import Logging
from causepy.config import setup as config
from causepy.config.api import Api as ConfigApi


Logging()

def run_server():
	""" Start the application
	"""
	site_config = ConfigApi()

	site_config.add_folder('data/pdfs')
	site_config.add_config({
		'/downloads': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': 'data/pdfs'
		}
	})

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
		'server.socket_port': config.PORT
	})

	run_server()
	cherrypy.engine.start()
