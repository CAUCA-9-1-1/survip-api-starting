import cherrypy

from cause.api.management.core.execute_api_class import ExecuteApiClass


class UrlForSurvey(ExecuteApiClass):
	@cherrypy.expose
	def survey(self, *args, **kwargs):
		return self.call_method('Survey', self.get_argument(args, kwargs))

	@cherrypy.expose
	def surveyquestion(self, *args, **kwargs):
		return self.call_method('SurveyQuestion', self.get_argument(args, kwargs))

	@cherrypy.expose
	def surveychoice(self, *args, **kwargs):
		return self.call_method('SurveyChoice', self.get_argument(args, kwargs))
