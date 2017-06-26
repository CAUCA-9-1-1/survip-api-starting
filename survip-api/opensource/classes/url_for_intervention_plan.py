import cherrypy
from framework.manage.api import Api as BaseApi


class UrlForInterventionPlan(BaseApi):
	@cherrypy.expose
	def alarmpaneltype(self, *args, **kwargs):
		return self.call_method('AlarmPanelType', self.get_argument(args, kwargs))