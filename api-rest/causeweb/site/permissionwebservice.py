import json
from .. import config
from ..session.static import Static as Session
from ..html.request import Request


class PermissionWebService:
	def get(self, feature_name=None):
		try:
			version = 'DEV' if config.PACKAGE_VERSION == '__package_version__' else config.PACKAGE_VERSION
			query = Request("http://%s/permission/%s" % (config.WEBSERVICE['host'], feature_name or ''), 'GET')
			data = json.loads(query.send(None, None, {
				'User-Agent': '%s/%s' % (config.PACKAGE_NAME, version),
				'Authorization': 'Token %s' % Session.get('access-token')
			}))

			return data['data']
		except:
			return {}