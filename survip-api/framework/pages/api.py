import json
import cherrypy
from ..manage.api import Api as BaseApi
from ..config import setup as config


class Api(BaseApi):
	class_name = ''
	method_name = ''

	@cherrypy.expose
	def index(self):
		return json.dumps({
			'name': config.PACKAGE_NAME,
			'version': config.PACKAGE_VERSION
		})

	@cherrypy.expose
	def auth(self, *args, **kwargs):
		return self.call_method('Auth', self.get_argument(args, kwargs))

	@cherrypy.expose
	def webuser(self, *args, **kwargs):
		return self.call_method('Webuser', self.get_argument(args, kwargs))