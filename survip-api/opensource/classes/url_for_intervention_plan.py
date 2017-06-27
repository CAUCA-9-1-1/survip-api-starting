import cherrypy
from framework.manage.api import Api as BaseApi


class UrlForInterventionPlan(BaseApi):
	@cherrypy.expose
	def alarmpaneltype(self, *args, **kwargs):
		return self.call_method('AlarmPanelType', self.get_argument(args, kwargs))

	@cherrypy.expose
	def constructiontype(self, *args, **kwargs):
		return self.call_method('ConstructionType', self.get_argument(args, kwargs))

	@cherrypy.expose
	def interventionplangeneralinformations(self, *args, **kwargs):
		return self.call_method('InterventionPlanGeneralInformations', self.get_argument(args, kwargs))