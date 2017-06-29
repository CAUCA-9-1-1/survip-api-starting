import cherrypy

from cause.api.management.core.execute_api_class import ExecuteApiClass


class UrlForInterventionPlan(ExecuteApiClass):
	@cherrypy.expose
	def alarmpaneltype(self, *args, **kwargs):
		return self.call_method('AlarmPanelType', self.get_argument(args, kwargs))

	@cherrypy.expose
	def constructiontype(self, *args, **kwargs):
		return self.call_method('ConstructionType', self.get_argument(args, kwargs))

	@cherrypy.expose
	def interventionplangeneralinformations(self, *args, **kwargs):
		return self.call_method('InterventionPlanGeneralInformations', self.get_argument(args, kwargs))