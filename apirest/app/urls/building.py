from causepy.manage.database import Database
from causepy.manage.multilang import MultiLang
from causepy.urls.base import Base
from ..mapping.building import Building as Table


class Building(Base):
	table_name = 'tbl_building'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_building=None):
		""" Return all building information

		:param id_building: UUID
		"""
		with Database() as db:
			if id_building is None:
				if self.has_permission('RightAdmin') is False:
					return self.no_access()

				data = db.query(Table).all()
			else:
				data = db.query(Table).get(id_building)

		return {
			'data': data
		}

	def modify(self, args):
		""" Modify all information for building

		:param args: {
			id_building: UUID,
			name: JSON
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with Database() as db:
			data = db.query(Table).filter(Table.id_building == args['id_building']).first()

			if 'name' in args:
				id_language_content = MultiLang.set(args['name'])
				data.id_language_content_name = id_language_content

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