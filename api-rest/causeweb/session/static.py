import json
import cherrypy
from .. import config
from ..html.request import Request
from ..html.json import JsonEncoder

if config.DATABASE is not None:
	from ..storage.db import DB


class Static:
	@staticmethod
	def get(key):
		if key not in cherrypy.session:
			return None

		return cherrypy.session[key]

	@staticmethod
	def set(key, value):
		cherrypy.session[key] = value

	@staticmethod
	def log(object=None, name=None, param=None):
		if 'userId' in cherrypy.session and cherrypy.session['userId'] is not None:
			param = param if isinstance(param, str) or param is None else json.dumps(param, cls=JsonEncoder)

			if config.WEBSERVICE is not None:
				version = 'DEV' if config.PACKAGE_VERSION == '__package_version__' else config.PACKAGE_VERSION
				query = Request("http://%s/useraction/" % config.WEBSERVICE['host'], 'PUT')
				query.send({
					'id_webuser': cherrypy.session['userId'],
					'object': object,
					'name': name,
					'param': param,
				}, None, {
					'User-Agent': '%s/%s' % (config.PACKAGE_NAME, version),
					'Authorization': 'Key %s' % config.WEBSERVICE['key']
				})
			elif config.DATABASE is not None:
				with DB() as db:
					db.execute("""INSERT INTO tbl_webuser_action(
								id_webuser_action, id_webuser, action_time, action_object, action_name, action_param
								) VALUES (uuid_generate_v4(), %s, NOW(), %s, %s, %s);""", (
						cherrypy.session['userId'], object, name, param
					))