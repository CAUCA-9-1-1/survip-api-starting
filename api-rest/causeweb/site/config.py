import os
import logging
import cherrypy
import importlib
from causeweb import config


class ConfigSite:
	def __init__(self, specific_base_config=None):
		self.cherrypy_version = int(cherrypy.__version__.split('.', 1)[0])
		self.site_config = {}
		self.base_config = {
			'tools.sessions.on': True,
			'tools.sessions.name': config.PACKAGE_NAME,
			'tools.sessions.storage_path': 'data/sessions',
			'tools.sessions.timeout': config.SESSION_TIMEOUT,
			'tools.sessions.secure': config.IS_SSL,
			'tools.sessions.httponly': True,
			'tools.staticdir.root': os.path.abspath(os.getcwd()),
			'log.screen': False,
		}
		self.static_config = {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': 'static'
		}
		self.causejs_config = {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': 'StaticWebContent',
			'tools.staticdir.root': os.path.abspath('../../')
		}

		self.create_basic_folder()
		self.check_uwsgi()
		self.config_session()

		if specific_base_config is not None:
			self.base_config.update(specific_base_config)

		self.add_config({
			'/': self.base_config
		})

		if os.path.exists("%s/static" % config.ROOT):
			self.add_config({
				'/static': self.static_config,
			})

		self.use_local_staticwebcontent()

	def create_basic_folder(self):
		self.add_folder('data')
		self.add_folder('data/logs')
		self.add_folder('data/sessions')

	def check_uwsgi(self):
		if config.USE_UWSGI is False:
			self.base_config.update({
				'log.access_file': '%s/data/logs/cherrypy_access.log' % config.ROOT,
				'log.error_file': '%s/data/logs/cherrypy_error.log' % config.ROOT,
			})

	def config_session(self):
		if self.cherrypy_version > 8:
			self.base_config.update({
				'tools.sessions.storage_class': cherrypy.lib.sessions.FileSession
			})
		else:
			self.base_config.update({
				'tools.sessions.storage_type': 'File'
			})

	def add_config(self, element):
		self.site_config.update(element)

	def add_folder(self, path):
		if not os.path.exists("%s/%s/" % (config.ROOT, path)):
			os.makedirs("%s/%s/" % (config.ROOT, path))

	def add_page(self, page, path=None):
		try:
			page_name = "app.pages.%s" % page.lower()
			page_loaded = importlib.import_module(page_name, 'app.pages')
			page_class = getattr(page_loaded, page)
			path = path if path is not None else '/%s' % page.lower()

			cherrypy.tree.mount(page_class(), path, self.site_config)
		except:
			logging.exception("Can't mount the page %s, config %s" % (page, self.site_config))

	def use_local_staticwebcontent(self):
		if config.MINIMIZE_JS is False:
			if not os.path.exists("%s/../../StaticWebContent" % config.ROOT) and not os.path.exists("%s/../../../StaticWebContent" % config.ROOT):
				raise Exception("We can't find StaticWebContent, set 'MINIMIZE_JS = True' in your config.py")
			if not os.path.exists("%s/../../StaticWebContent" % config.ROOT):
				self.causejs_config['tools.staticdir.root'] = os.path.abspath('../../../')

			self.add_config({
				'/causeJs': self.causejs_config
			})

	def complete(self):
		if os.path.exists("%s/app/pages/%s.py" % (config.ROOT, 'root')):
			self.add_page('Root', '/')

		if os.path.exists("%s/app/pages/%s.py" % (config.ROOT, 'js')):
			self.add_page('Js')

		if os.path.exists("%s/app/pages/%s.py" % (config.ROOT, 'ajax')):
			self.add_page('Ajax')

		self.add_config({
			'server.environment': 'production' if config.IS_DEV is False else 'test_suite',
			'request.show_tracebacks': config.IS_DEV,
		})