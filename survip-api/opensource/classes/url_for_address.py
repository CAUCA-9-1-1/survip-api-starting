import cherrypy
from framework.manage.api import Api as BaseApi


class UrlForAddress(BaseApi):
	@cherrypy.expose
	def lane(self, *args, **kwargs):
		return self.call_method('Lane', self.get_argument(args, kwargs))

	@cherrypy.expose
	def citylanes(self, *args, **kwargs):
		return self.call_method('CityLanes', self.get_argument(args, kwargs))

	@cherrypy.expose
	def lanelight(self, *args, **kwargs):
		return self.call_method('LaneLight', self.get_argument(args, kwargs))

	@cherrypy.expose
	def city(self, *args, **kwargs):
		return self.call_method('City', self.get_argument(args, kwargs))

	@cherrypy.expose
	def citytype(self, *args, **kwargs):
		return self.call_method('CityType', self.get_argument(args, kwargs))

	@cherrypy.expose
	def county(self, *args, **kwargs):
		return self.call_method('County', self.get_argument(args, kwargs))

	@cherrypy.expose
	def region(self, *args, **kwargs):
		return self.call_method('Region', self.get_argument(args, kwargs))

	@cherrypy.expose
	def state(self, *args, **kwargs):
		return self.call_method('State', self.get_argument(args, kwargs))

	@cherrypy.expose
	def country(self, *args, **kwargs):
		return self.call_method('Country', self.get_argument(args, kwargs))