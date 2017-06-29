import cherrypy

from cause.api.survip.api_url import ApiUrl as UrlForSurviP


class ApiUrl(UrlForSurviP):
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
