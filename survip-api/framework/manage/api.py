import re
import os
import json
import logging
import cherrypy
import importlib.util
from sqlalchemy.ext.declarative import DeclarativeMeta
from ..manage.json import JsonEncoder
from ..auth.token import Token
from ..config import setup as config

class Api:
	class_name = ''
	method_name = ''

	def load_class(self, name):
		folders = ['app', 'opensource', 'framework']
		for folder in folders:
			class_object = self.load_class_from(folder, name)

			if class_object is not None:
				break

		if class_object is None:
			raise Exception("We can't find the class: %s" % name)
		else:
			return class_object

	def load_class_from(self, folder, name):
		self.class_name = "%s.resturls.%s" % (folder, name.lower())
		file = '%s/%s.py' % (config.ROOT, self.class_name.replace('.', '/'))

		if os.path.isfile(file):
			try:
				class_load = importlib.import_module(self.class_name, '%s.resturls' % folder)
				class_object = getattr(class_load, name)

				return class_object
			except Exception as e:
				raise Exception("Loading exception on class '%s': %s" % (name, e))

		return None

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

		if Token().valid_access_from_header() is True or (name == 'Auth' and cherrypy.request.method == 'PUT'):
			execute = getattr(class_object, 'every_execution', None)
			execute(class_object(), name, cherrypy.request.method, *args)

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
				'error': ''
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
		arguments = ()

		try:
			body = cherrypy.request.body.readlines()

			if body[0] is not '':
				args = json.loads(body[0].decode('utf-8'))

				if config.FORCE_CAMELCASE:
					arguments = (self.convert_from_camel_case(args),)
				else:
					arguments = (args,)
		except Exception as e:
			if args:
				arguments = ()
				for val in args:
					arguments = arguments + (self.convert_argument(val),)
			if kwargs:
				if config.FORCE_CAMELCASE:
					kwargs = self.convert_from_camel_case(self.convert_argument(kwargs))

				arguments = (kwargs,)

		return arguments

	def convert_from_camel_case(self, data):
		for old_key in data:
			if sum(1 for c in old_key if c.isupper()):
				key = re.sub(r'[A-Z]', lambda x: '_' + x.group(0).lower(), old_key)
				data[key] = data.pop(old_key)
			else:
				key = old_key

			if isinstance(data[key], list):
				for pos, val in enumerate(data[key]):
					data[key][pos] = self.convert_from_camel_case(val)
			elif isinstance(data[key], dict):
				data[key] = self.convert_from_camel_case(data[key])

		return data

	def convert_to_camel_case(self, data):
		new_data = dict()

		if isinstance(data, object) and isinstance(data.__class__, DeclarativeMeta):
			data = JsonEncoder.sqlalchemy_to_dict(data)

		if isinstance(data, dict):
			for old_key in data:
				if '_' in old_key:
					key = re.sub(r'_([a-z])', lambda x: x.group(1).upper(), old_key)
				else:
					key = old_key

				if isinstance(data[old_key], tuple):
					info = ()
					for pos, val in enumerate(data[old_key]):
						info = info + (self.convert_to_camel_case(val),)
					new_data[key] = info
				elif isinstance(data[old_key], list):
					info = list()
					for pos, val in enumerate(data[old_key]):
						info.append(self.convert_to_camel_case(val))
					new_data[key] = info
				elif isinstance(data[old_key], dict):
					new_data[key] = self.convert_to_camel_case(data[old_key])
				else:
					new_data[key] = data[old_key]

		return new_data

	def convert_argument(self, val):
		if val == '' or val == 'null':
			return None
		elif val == 'true':
			return True
		elif val == 'false':
			return False

		return val