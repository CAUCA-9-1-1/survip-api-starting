from cause.api.management.resturls.base import Base

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
        'PUT': 'modify',
        'POST': '',
        'DELETE': '',
        'PATCH': '',
    }

    def get(self, id_test=None, is_active=None):
        return {
            'method test': 'GET'
        }

    def modify(self, args={}):
        return {
            'method test': 'PUT'
        }
