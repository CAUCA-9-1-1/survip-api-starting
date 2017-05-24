import importlib.util
import json
import logging

import cherrypy
from sqlalchemy.ext.declarative import DeclarativeMeta

from causepy.manage.json import JsonEncoder
from ..auth.token import Token
from ..config import setup as config


class Api:
	class_name = ''
	method_name = ''

	@cherrypy.expose
	def index(self):
		return json.dumps({
			'name': config.PACKAGE_NAME,
			'version': config.PACKAGE_VERSION
		})

	def load_class(self, name):
		try:
			self.class_name = "apirest.app.urls.%s" % name.lower()
			class_load = importlib.import_module(self.class_name, 'apirest.app.urls')
			class_object = getattr(class_load, name)

			return class_object
		except:
			try:
				self.class_name = "causepy.urls.%s" % name.lower()
				class_load = importlib.import_module(self.class_name, 'causepy.urls')
				class_object = getattr(class_load, name)

				return class_object
			except:
				raise Exception("We can't find the class '%s'" % (name))

	def exec_method(self, name, args):
		class_object = self.load_class(name)
		method_mapping = getattr(class_object, 'mapping_method', None)
		self.method_name = cherrypy.request.method.lower()

		if method_mapping is not None:
			if cherrypy.request.method in method_mapping and method_mapping[cherrypy.request.method]:
				self.method_name = method_mapping[cherrypy.request.method]

		api_method = getattr(class_object, self.method_name, None)

		if api_method is None:
			raise Exception("We can't find the method '%s' on class '%s'" % (cherrypy.request.method, name))

		if Token().valid_access_from_header() is True:
			execute = getattr(class_object, 'every_execution', None)
			execute(class_object(), cherrypy.request.method, *args)

			return api_method(class_object(), *args)
		else:
			return {
				'success': False,
				'login': False,
				'error': "Login failed",
			}

	def call_method(self, name, args):
		if cherrypy.request.method == 'OPTIONS':
			return json.dumps({
				'success': True,
				'error': '',
			})

		try:
			data = {
				'success': True,
				'error': '',
				'data': None
			}
			return_data = self.exec_method(name, args)

			if isinstance(return_data, dict) and config.FORCE_CAMELCASE:
				return_data = self.convert_to_camel_case(return_data)

			data.update(return_data)

			return json.dumps(data, cls=JsonEncoder)
		except Exception as e:
			logging.exception("Error from api class")

			return json.dumps({
				'success': False,
				'error': e,
				'data': None
			}, cls=JsonEncoder)

	def get_argument(self, args, kwargs):
		try:
			body = cherrypy.request.body.readlines()

			if body[0] is not '':
				return (json.loads(body[0].decode('utf-8')),)
		except:
			if args:
				arguments = ()
				for val in args:
					arguments = arguments + (self.convert_argument(val),)

				return arguments
			if kwargs:
				for key in kwargs:
					kwargs[key] = self.convert_argument(kwargs[key])

				return (kwargs,)

		return ()

	def convert_to_camel_case(self, data):
		if isinstance(data, object) and isinstance(data.__class__, DeclarativeMeta):
			data = JsonEncoder.sqlalchemy_to_dict(data)

		for old_key in data:
			if '_' in old_key:
				word = old_key.split('_')
				key = word[0] + "".join(x.title() for x in word[1:])
				data[key] = data.pop(old_key)
			else:
				key = old_key

			if isinstance(data[key], list):
				for pos, val in enumerate(data[key]):
					data[key][pos] = self.convert_to_camel_case(val)
			elif isinstance(data[key], dict):
				data[key] = self.convert_to_camel_case(data[key])

		return data

	def convert_argument(self, val):
		if val == '' or val == 'null':
			return None
		elif val == 'true':
			return True
		elif val == 'false':
			return False

		return val