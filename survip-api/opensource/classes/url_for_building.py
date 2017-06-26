import cherrypy
from framework.manage.api import Api as BaseApi


class UrlForBuilding(BaseApi):
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
	def risklevel(self, *args, **kwargs):
		return self.call_method('RiskLevel', self.get_argument(args, kwargs))

	@cherrypy.expose
	def risklevellist(self, *args, **kwargs):
		return self.call_method('RiskLevelList', self.get_argument(args, kwargs))

	@cherrypy.expose
	def utilisationcode(self, *args, **kwargs):
		return self.call_method('UtilisationCode', self.get_argument(args, kwargs))
