import uuid
from cause.api.management.core.manage.database import Database
from cause.api.management.resturls.base import Base
from ..models.fire_hydrant import FireHydrant as Table


class FireHydrant(Base):
	table_name = 'tbl_fire_hydrant'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_fire_hydrant=None, is_active=None):
		""" Return all information for fire hydrant

		:param id_fire_hydrant: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_fire_hydrant is None and is_active is None:
				data = db.query(Table).all()
			elif id_fire_hydrant is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_fire_hydrant)

		return {
			'data': data
		}


	def create(self, args):
		""" Create a new fire hydrant

		:param args: {
			id_fire_hydrant_type: JSON,
			id_lane: UUID,
			id_intersection: UUID,
			altitude: FLOAT,
			fire_hydrant_number: STRING,
			id_operator_type_rate: UUID,
			rate_from: STRING,
			rate_to: STRING,
			id_unit_of_measure_rate: UUID,
			id_operator_type_pressure: UUID,
			pressure_from: STRING,
			pressure_to: STRING,
			id_unit_of_measure_pressure: UUID,
			color: STRING,
			comments: STRING,
			physical_position: STRING,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'id_fire_hydrant_type' not in args or 'fire_hydrant_number' not in args:
			raise Exception("You need to pass a 'fire_hydrant_number' and 'id_fire_hydrant_type'")

		id_fire_hydrant = uuid.uuid4()
		id_lane = args['id_lane'] if 'id_lane' in args else None
		id_intersection = args['id_intersection'] if 'id_intersection' in args else None

		with Database() as db:
			db.insert(Table(id_fire_hydrant, args['id_fire_hydrant_type'], args['fire_hydrant_number'],
			                id_lane, id_intersection))
			db.commit()

		return {
			'id_fire_hydrant': id_fire_hydrant,
			'message': 'fire hydrant successfully created'
		}

	def modify(self, args):
		""" Modify a fire hydrant

		:param args: {
			id_fire_hydrant_type: JSON,
			id_lane: UUID,
			id_intersection: UUID,
			altitude: FLOAT,
			fire_hydrant_number: STRING,
			id_operator_type_rate: UUID,
			rate_from: STRING,
			rate_to: STRING,
			id_unit_of_measure_rate: UUID,
			id_operator_type_pressure: UUID,
			pressure_from: STRING,
			pressure_to: STRING,
			id_unit_of_measure_pressure: UUID,
			color: STRING,
			comments: STRING,
			physical_position: STRING,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		if 'id_fire_hydrant' not in args:
			raise Exception("You need to pass a id_fire_hydrant")

		with Database() as db:
			data = db.query(Table).get(args['id_fire_hydrant'])

			if 'id_fire_hydrant_type' in args:
				data.id_fire_hydrant_type = args['id_fire_hydrant_type']
			if 'fire_hydrant_number' in args:
				data.fire_hydrant_number = args['fire_hydrant_number']
			if 'id_lane' in args:
				data.id_lane = args['id_lane']
			if 'id_intersection' in args:
				data.id_intersection = args['id_intersection']
			if 'altitude' in args:
				data.altitude = args['altitude']
			if 'id_operator_type_rate' in args:
				data.id_operator_type_rate = args['id_operator_type_rate']
			if 'from_rate' in args:
				data.from_rate = args['from_rate']
			if 'to_rate' in args:
				data.to_rate = args['to_rate']
			if 'id_unit_of_measure_rate' in args:
				data.id_unit_of_measure_rate = args['id_unit_of_measure_rate']
			if 'id_operator_type_pressure' in args:
				data.id_operator_type_pressure = args['id_operator_type_pressure']
			if 'from_pressure' in args:
				data.from_pressure = args['from_pressure']
			if 'to_pressure' in args:
				data.to_pressure = args['to_pressure']
			if 'id_unit_of_measure_pressure' in args:
				data.id_unit_of_measure_pressure = args['id_unit_of_measure_pressure']
			if 'color' in args:
				data.color = args['color']
			if 'comments' in args:
				data.comments = args['comments']
			if 'physical_position' in args:
				data.physical_position = args['physical_position']
			if 'is_active' in args:
				data.is_active = args['is_active']

			db.commit()

		return {
			'message': 'fire hydrant successfully modified'
		}

	def remove(self, id_fire_hydrant):
		""" Remove a fire hydrant

		:param id_fire_hydrant: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			return self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_fire_hydrant)
			data.is_active = False
			db.commit()

		return {
			'message': 'fire hydrant successfully removed'
		}