import cherrypy
from causepy.pages.api import Api as BaseApi


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
