from causeweb.storage.db import DB
from causeweb.apis.base import Base


class BuildingPersonRequiringAssistance(Base):
	mapping_method = {
		'GET': 'get',
		'PUT': 'assign',
		'POST': 'modify',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_building):
		""" Return all PRSA for one building

		:param id_building: UUID
		"""
		with DB() as db:
			data = db.get_all("SELECT * FROM tbl_building_person_requiring_assistance WHERE id_building=%s;", (id_building,))

		return {
			'data': data
		}

	def assign(self, args):
		""" Assign new PRSA to building

		:param args: {
			id_building: UUID,
		}
		"""
		with DB() as db:
			db.execute("""INSERT INTO tbl_building_person_requiring_assistance (
							id_building_person_requiring_assistance, id_building, number_of_day_residents, number_of_night_residents,
							number_of_evening_residents, description, is_active
						  ) VALUES(uuid_generate_v4(), %s, %s, %s, %s, %s, True);""", (
				args['id_building'], args['number_of_day_residents'], args['number_of_night_residents'], args['number_of_evening_residents'], args['description']
			))

		return {
			'message': 'building person requiring assistance successfully assigned'
		}

	def modify(self, args):
		""" Modify all information for building person requiring assistance

		:param args: {
			id_building_person_requiring_assistance: UUID,
		}
		"""
		with DB() as db:
			db.execute("""UPDATE tbl_building_person_requiring_assistance SET
							number_of_day_residents=%s, number_of_night_residents=%s, number_of_evening_residents=%s, description=%s
						  WHERE id_building_person_requiring_assistance=%s;""", (
				args['number_of_day_residents'], args['number_of_night_residents'], args['number_of_evening_residents'],
				args['description'], args['id_building_person_requiring_assistance']
			))

		return {
			'message': 'building person requiring assistance modified'
		}

	def remove(self, id_building_person_requiring_assistance):
		""" Remove building person requiring assistance

		:param id_building_person_requiring_assistance: UUID
		"""
		with DB() as db:
			db.execute("UPDATE tbl_building_person_requiring_assistance SET is_active=%s WHERE id_building_person_requiring_assistance=%;", (
				False, id_building_person_requiring_assistance
			))

		return {
			'message': 'building person requiring assistance successfully removed'
		}