import uuid
from framework.manage.database import Database
from framework.manage.multilang import MultiLang
from framework.resturls.base import Base
from ..models.lane import Lane as Table


class Lane(Base):
	table_name = 'tbl_lane'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_lane=None, is_active=None):
		""" Return all lane information

		:param id_lane: UUID
		:param is_active: Boolean
		"""
		with Database() as db:
			if id_lane is None and is_active is None:
				data = db.query(Table).all()
			elif id_lane is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_lane)

		return {
			'data': data
		}

	def create(self, args):
		""" Create a new lane

		:param args: {
			name: JSON,
			id_city: UUID
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		id_lane = uuid.uuid4()
		id_language_content = MultiLang.set(args['name'], True)

		with Database() as db:
			db.insert(Table(id_lane, id_language_content, args['id_city'],
			                args['public_lane_code'], args['generic_code']))
			db.commit()

		return {
			'id_lane': id_lane,
			'message': 'lane successfully created'
		}

	def modify(self, args):
		""" Modify a lane

		:param args: {
			id_lane: UUID,
			name: JSON,
			id_city: UUID,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'id_lane' not in args:
			raise Exception("You need to pass a id_lane")

		with Database() as db:
			data = db.query(Table).filter(Table.id_lane == args['id_lane']).first()

			if 'name' in args:
				data.id_language_content_name = MultiLang.set(args['name'])
			if 'id_city' in args:
				data.id_city = args['id_city']
			if 'public_lane_code' in args:
				data.public_lane_code = args['public_lane_code']
			if 'generic_code' in args:
				data.generic_code = args['generic_code']

			db.commit()

		return {
			'message': 'lane successfully modify'
		}

	def remove(self, id_lane):
		""" Remove a lane

		:param id_lane: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with Database() as db:
			data = db.query(Table).filter(Table.id_lane == id_lane).first()
			data.is_active = False
			db.commit()

		return {
			'message': 'lane successfully removed'
		}