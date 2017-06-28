import cherrypy

from cause.api.management.core.manage.api import Api as BaseApi


class UrlForInspection(BaseApi):
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