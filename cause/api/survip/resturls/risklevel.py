import uuid
from cause.api.management.core.manage.database import Database
from cause.api.management.core.manage.multilang import MultiLang
from cause.api.management.resturls.base import Base
from ..models.risk_level import RiskLevel as Table


class RiskLevel(Base):
	table_name = 'tbl_risk_level'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_risk_level=None, is_active=None):
		""" Return all information for risk level

		:param id_risk_level: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_risk_level is None and is_active is None:
				data = db.query(Table).all()
			elif id_risk_level is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_risk_level)

		return {
			'data': data
		}


	def create(self, args):
		""" Create a new risk level

		:param args: {
			name: JSON,
			sequence: INTEGER,
			code: INTEGER,
			color: STRING,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'code' not in args or 'name' not in args:
			raise Exception("You need to pass a 'name' and 'code'")

		id_risk_level = uuid.uuid4()
		id_language_content = MultiLang.set(args['name'], True)
		sequence = args['sequence'] if 'sequence' in args else None
		color = args['color'] if 'color' in args else None

		with Database() as db:
			db.insert(Table(id_risk_level, id_language_content, sequence, args['code'], color))
			db.commit()

		return {
			'id_risk_level': id_risk_level,
			'message': 'risk level successfully created'
		}

	def modify(self, args):
		""" Modify a risk level

		:param args: {
			id_risk_level: UUID,
			name: JSON,
			sequence: INTEGER,
			code: INTEGER,
			color: STRING,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'id_risk_level' not in args:
			raise Exception("You need to pass a id_risk_level")

		with Database() as db:
			data = db.query(Table).get(args['id_risk_level'])

			if 'name' in args:
				data.id_language_content_name = MultiLang.set(args['name'])
			if 'sequence' in args:
				data.sequence = args['sequence']
			if 'code' in args:
				data.code = args['code']
			if 'color' in args:
				data.color = args['color']
			if 'is_active' in args:
				data.is_active = args['is_active']

			db.commit()

		return {
			'message': 'risk level successfully modified'
		}

	def remove(self, id_risk_level):
		""" Remove a risk level

		:param id_risk_level: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_risk_level)
			data.is_active = False
			db.commit()

		return {
			'message': 'risk level successfully removed'
		}