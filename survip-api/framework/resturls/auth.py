from .base import Base
from .webuser import Webuser
from framework.auth.token import Token


class Auth(Token, Base):
	expires_in_minutes = 120
	mapping_method = {
		'GET': 'token',
		'PUT': 'logon',
		'POST': 'register',
		'DELETE': '',
		'PATCH': '',
	}

	def token(self, token=None):
		if token is None:
			raise Exception("You need to pass a token id")

		return {
			'message': 'token is valid'
		}

	def register(self, args):
		Webuser().create(args)

		return {
			'message': 'user successfully saved'
		}
