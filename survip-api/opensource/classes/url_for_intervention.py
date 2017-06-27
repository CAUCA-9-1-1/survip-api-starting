import cherrypy
from framework.manage.api import Api as BaseApi


class UrlForIntervention(BaseApi):
	@cherrypy.expose
	def interventiondetailgeneralinformations(self, *args, **kwargs):
		return self.call_method('InterventionPlanGeneralInformations', self.get_argument(args, kwargs))