import cherrypy
from ..classes.url_for_address import UrlForAddress
from ..classes.url_for_building import UrlForBuilding
from ..classes.url_for_firehydrant import UrlForFireHydrant
from ..classes.url_for_inspection import UrlForInspection
from ..classes.url_for_intervention_plan import UrlForInterventionPlan
from ..classes.url_for_survey import UrlForSurvey
from cause.api.management.pages.api import Api as ManagementApi


class Api(UrlForSurvey, UrlForInterventionPlan, UrlForInspection,
          UrlForFireHydrant, UrlForAddress, UrlForBuilding, ManagementApi):
	@cherrypy.expose
	def firesafetydepartment(self, *args, **kwargs):
		return self.call_method('FireSafetyDepartment', self.get_argument(args, kwargs))

	@cherrypy.expose
	def webuserfiresafetydepartment(self, *args, **kwargs):
		return self.call_method('WebuserFireSafetyDepartment', self.get_argument(args, kwargs))

	@cherrypy.expose
	def picture(self, *args, **kwargs):
		return self.call_method('Picture', self.get_argument(args, kwargs))