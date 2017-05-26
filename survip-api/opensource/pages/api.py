import cherrypy
from opensource.classes.url_for_address import UrlForAddress
from opensource.classes.url_for_building import UrlForBuilding
from opensource.classes.url_for_inspection import UrlForInspection
from framework.pages.api import Api as FrameworkApi


class Api(UrlForInspection, UrlForAddress, UrlForBuilding, FrameworkApi):
	pass
