import cherrypy

from cause.api.management.core.execute_api_class import ExecuteApiClass


class UrlForInspection(ExecuteApiClass):
	@cherrypy.expose
	def inspection(self, *args, **kwargs):
		return self.call_method('Inspection', self.get_argument(args, kwargs))

	@cherrypy.expose
	def inspectionanswer(self, *args, **kwargs):
		return self.call_method('InspectionAnswer', self.get_argument(args, kwargs))

	@cherrypy.expose
	def inspectionbuilding(self, *args, **kwargs):
		return self.call_method('InspectionBuilding', self.get_argument(args, kwargs))

	@cherrypy.expose
	def inspectionbyuser(self, *args, **kwargs):
		return self.call_method('InspectionByUser', self.get_argument(args, kwargs))

	@cherrypy.expose
	def inspectionreport(self, *args, **kwargs):
		return self.call_method('InspectionReport', self.get_argument(args, kwargs))

	@cherrypy.expose
	def inspectionstatistic(self, *args, **kwargs):
		return self.call_method('InspectionStatistic', self.get_argument(args, kwargs))