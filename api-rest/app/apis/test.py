from causeweb.apis.base import Base

""" Basic example

class Test(Base):
	def GET(self, action, entry):
		return {
			'method test1': 'GET'
		}

	def POST(self, args):
		return {
			'method test1': 'POST'
		}
"""

""" More complete example
"""
class Test(Base):
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': 'modify',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, action, entry):
		return {
			'method test2': 'GET'
		}

	def modify(self, args):
		return {
			'method test2': 'POST'
		}