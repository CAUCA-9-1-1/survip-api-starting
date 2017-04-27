from causeweb.site.token import Token
from causeweb.apis.webuser import Webuser
from causeweb.apis.base import Base


class Auth(Token, Base):
	expires_in_minutes = 120
	mapping_method = {
		'GET': 'token',
		'PUT': 'logon',
		'POST': 'register',
		'DELETE': '',
		'PATCH': '',
	}

	def token(self, args):
		return {
			'message': 'token is valid'
		}

	def register(self, args):
		Webuser().create(args)

		return {
			'message': 'user successfully saved'
		}
