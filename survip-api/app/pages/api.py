import cherrypy
from opensource.pages.api import Api as OpenSourceApi


class Api(OpenSourceApi):
	@cherrypy.expose
	def multilang(self, *args, **kwargs):
		return self.call_method('Multilang', self.get_argument(args, kwargs))

	@cherrypy.expose
	def search(self, *args, **kwargs):
		return self.call_method('Search', self.get_argument(args, kwargs))

	@cherrypy.expose
	def interventionplan(self, *args, **kwargs):
		return self.call_method('InterventionPlan', self.get_argument(args, kwargs))

	@cherrypy.expose
	def interventionplanfirehydrant(self, *args, **kwargs):
		return self.call_method('InterventionPlanFireHydrant', self.get_argument(args, kwargs))

	@cherrypy.expose
	def interventionplanstructure(self, *args, **kwargs):
		return self.call_method('InterventionPlanStructure', self.get_argument(args, kwargs))

	@cherrypy.expose
	def firesafetydepartmentcityserving(self, *args, **kwargs):
		return self.call_method('FireSafetyDepartmentCityServing', self.get_argument(args, kwargs))

	@cherrypy.expose
	def userfiresafetydepartment(self, *args, **kwargs):
		return self.call_method('WebuserFireSafetyDepartment', self.get_argument(args, kwargs))