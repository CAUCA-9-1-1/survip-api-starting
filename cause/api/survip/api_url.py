import cherrypy

from cause.api.management.api_url import ApiUrl as UrlForManagement
from cause.api.survip.url_by_module.address import UrlForAddress
from cause.api.survip.url_by_module.building import UrlForBuilding
from cause.api.survip.url_by_module.firehydrant import UrlForFireHydrant
from cause.api.survip.url_by_module.inspection import UrlForInspection
from cause.api.survip.url_by_module.intervention_plan import UrlForInterventionPlan
from cause.api.survip.url_by_module.survey import UrlForSurvey


class ApiUrl(UrlForSurvey, UrlForInterventionPlan, UrlForInspection,
             UrlForFireHydrant, UrlForAddress, UrlForBuilding, UrlForManagement):
	@cherrypy.expose
	def firesafetydepartment(self, *args, **kwargs):
		return self.call_method('FireSafetyDepartment', self.get_argument(args, kwargs))

	@cherrypy.expose
	def webuserfiresafetydepartment(self, *args, **kwargs):
		return self.call_method('WebuserFireSafetyDepartment', self.get_argument(args, kwargs))

	@cherrypy.expose
	def picture(self, *args, **kwargs):
		return self.call_method('Picture', self.get_argument(args, kwargs))