import cherrypy
from opensource.classes.url_for_address import UrlForAddress
from opensource.classes.url_for_building import UrlForBuilding
from opensource.classes.url_for_inspection import UrlForInspection
from opensource.classes.url_for_survey import UrlForSurvey
from framework.pages.api import Api as FrameworkApi


class Api(UrlForSurvey, UrlForInspection, UrlForAddress, UrlForBuilding, FrameworkApi):
	@cherrypy.expose
	def firesafetydepartment(self, *args, **kwargs):
		return self.call_method('FireSafetyDepartment', self.get_argument(args, kwargs))