import uuid
from cause.api.management.core.manage.database import Database
from cause.api.management.core.manage.multilang import MultiLang
from cause.api.management.resturls.base import Base
from ..models.building import BuildingFull as Table


class Building(Base):
	table_name = 'tbl_building'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_building=None, is_active=None):
		""" Return all building information

		:param id_building: UUID
		:param is_active: Boolean
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with Database() as db:
			if id_building is None:
				if is_active is None:
					data = db.query(Table).all()
				else:
					data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_building)

		return {
			'data': data
		}

	def create(self, args):
		""" Create a new building

		:param args: {
			name: JSON,
			id_lane: UUID
			civic_number: STRING
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		id_building = uuid.uuid4()
		id_language_content = MultiLang.set(args['name'], True)

		with Database() as db:
			db.insert(Table(id_building, id_language_content, args['civic_number']))
			db.commit()

		return {
			'id_building': id_building,
			'message': 'building successfully created'
		}

	def modify(self, args):
		""" Modify all information for building

		:param args: {
			id_building: UUID,
			name: JSON,
			civic_number: STRING
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'id_building' not in args:
			raise Exception("You need to pass a id_building")

		with Database() as db:
			data = db.query(Table).get(args['id_building'])

			if 'name' in args:
				data.id_language_content_name = MultiLang.set(args['name'])
			if 'civic_number' in args:
				data.civic_number = args['civic_number']
			if 'year_of_construction' in args:
				data.year_of_construction = args['year_of_construction']
			if 'building_value' in args:
				data.building_value = args['building_value']
			if 'number_of_floors' in args:
				data.number_of_floors = args['number_of_floors']
			if 'number_of_appartment' in args:
				data.number_of_appartment = args['number_of_appartment']

			db.commit()

		return {
			'message': 'building successfully modified'
		}

	def remove(self, id_building):
		""" Remove building

		:param id_building: UUID
		"""
		if self.has_permission('RightTPI') is False:
			return self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_building)
			data.is_active = False
			db.commit()

		return {
			'message': 'building successfully removed'
		}