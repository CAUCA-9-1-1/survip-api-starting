from causeweb.site.multilang import MultiLang
from .base import Base


class Multilang(Base):
	mapping_method = {
		'GET': '',
		'PUT': 'modify',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def modify(self, args):
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		MultiLang.modify(args['id_language_content'], args)

		return {
			'message': 'multilang successfully modify'
		}
