import cherrypy
from framework.manage.api import Api as BaseApi


class UrlForFireHydrant(BaseApi):
	@cherrypy.expose
	def firehydrant(self, *args, **kwargs):
		return self.call_method('FireHydrant', self.get_argument(args, kwargs))

	@cherrypy.expose
	def firehydranttype(self, *args, **kwargs):
		return self.call_method('FireHydrantType', self.get_argument(args, kwargs))

	@cherrypy.expose
	def operatortype(self, *args, **kwargs):
		return self.call_method('OperatorType', self.get_argument(args, kwargs))

	@cherrypy.expose
	def unitofmeasure(self, *args, **kwargs):
		return self.call_method('UnitOfMeasure', self.get_argument(args, kwargs))
