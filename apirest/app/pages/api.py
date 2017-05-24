import cherrypy
from causepy.pages.api import Api as BaseApi
from apirest.classes.url_for_address import UrlForAddress


class Api(UrlForAddress, BaseApi):
	@cherrypy.expose
	def auth(self, *args, **kwargs):
		return self.call_method('Auth', self.get_argument(args, kwargs))

	@cherrypy.expose
	def multilang(self, *args, **kwargs):
		return self.call_method('Multilang', self.get_argument(args, kwargs))

	@cherrypy.expose
	def apisaction(self, *args, **kwargs):
		return self.call_method('ApisAction', self.get_argument(args, kwargs))

	@cherrypy.expose
	def user(self, *args, **kwargs):
		return self.call_method('Webuser', self.get_argument(args, kwargs))

	@cherrypy.expose
	def useraction(self, *args, **kwargs):
		return self.call_method('WebuserAction', self.get_argument(args, kwargs))

	@cherrypy.expose
	def userstatistics(self, *args, **kwargs):
		return self.call_method('WebuserStatistics', self.get_argument(args, kwargs))

	@cherrypy.expose
	def permission(self, *args, **kwargs):
		return self.call_method('Permission', self.get_argument(args, kwargs))

	@cherrypy.expose
	def permissionuser(self, *args, **kwargs):
		return self.call_method('PermissionUser', self.get_argument(args, kwargs))

	@cherrypy.expose
	def inspection(self, *args, **kwargs):
		return self.call_method('Inspection', self.get_argument(args, kwargs))

	@cherrypy.expose
	def inspectionanswer(self, *args, **kwargs):
		return self.call_method('InspectionAnswer', self.get_argument(args, kwargs))

	@cherrypy.expose
	def inspectionreport(self, *args, **kwargs):
		return self.call_method('InspectionReport', self.get_argument(args, kwargs))

	@cherrypy.expose
	def inspectionstatistics(self, *args, **kwargs):
		return self.call_method('InspectionStatistics', self.get_argument(args, kwargs))

	@cherrypy.expose
	def survey(self, *args, **kwargs):
		return self.call_method('Survey', self.get_argument(args, kwargs))

	@cherrypy.expose
	def surveyquestion(self, *args, **kwargs):
		return self.call_method('SurveyQuestion', self.get_argument(args, kwargs))

	@cherrypy.expose
	def surveychoice(self, *args, **kwargs):
		return self.call_method('SurveyChoice', self.get_argument(args, kwargs))

	@cherrypy.expose
	def search(self, *args, **kwargs):
		return self.call_method('Search', self.get_argument(args, kwargs))

	@cherrypy.expose
	def building(self, *args, **kwargs):
		return self.call_method('Building', self.get_argument(args, kwargs))

	@cherrypy.expose
	def buildingcontact(self, *args, **kwargs):
		return self.call_method('BuildingContact', self.get_argument(args, kwargs))

	@cherrypy.expose
	def buildingpersonrequiringassistance(self, *args, **kwargs):
		return self.call_method('BuildingPersonRequiringAssistance', self.get_argument(args, kwargs))

	@cherrypy.expose
	def buildinghazardousmaterial(self, *args, **kwargs):
		return self.call_method('BuildingHazardousMaterial', self.get_argument(args, kwargs))

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
	def firesafetydepartment(self, *args, **kwargs):
		return self.call_method('FireSafetyDepartment', self.get_argument(args, kwargs))

	@cherrypy.expose
	def firesafetydepartmentcityserving(self, *args, **kwargs):
		return self.call_method('FireSafetyDepartmentCityServing', self.get_argument(args, kwargs))

	@cherrypy.expose
	def userfiresafetydepartment(self, *args, **kwargs):
		return self.call_method('WebuserFireSafetyDepartment', self.get_argument(args, kwargs))