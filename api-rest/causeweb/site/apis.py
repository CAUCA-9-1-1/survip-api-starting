import re
import json
import logging
import cherrypy
import importlib
from causeweb import config
from causeweb.site.token import Token
from causeweb.html.json import JsonEncoder
from causeweb.session.general import Session


class Apis:
	class_name = ''
	method_name = ''

	def load_class(self, name):
		try:
			self.class_name = "app.apis.%s" % name.lower()
			class_load = importlib.import_module(self.class_name, 'app.apis')
			class_object = getattr(class_load, name)

			return class_object
		except:
			try:
				self.class_name = "causeweb.apis.%s" % name.lower()
				class_load = importlib.import_module(self.class_name, 'causeweb.apis')
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
				'name': self.name,
				'success': False,
				'login': False,
				'error': "Login failed",
			}

	def call_method(self, name, args):
		if cherrypy.request.method == 'OPTIONS':
			return json.dumps({
				'name': self.name,
				'success': True,
				'error': '',
			})

		try:
			data = {
				'name': self.name,
				'success': True,
				'error': '',
			}
			return_data = self.exec_method(name, args)

			if isinstance(return_data, dict):
				data.update(self.convert_to_camel_case(return_data))

			Session.log(self.class_name, self.method_name, {
				'application': config.PACKAGE_NAME,
				'platform': cherrypy.request.headers.get('User-Agent', ''),
				'sessionId': cherrypy.session.id,
				'userIp': Session.get('userIp'),
				'arguments': args
			})

			return json.dumps(data, cls=JsonEncoder)
		except Exception as e:
			logging.exception("Error from api class")

			return json.dumps({
				'name': self.name,
				'success': False,
				'error': e,
				'data': ''
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