from causeweb.storage.db import DB
from causeweb.apis.base import Base


class BuildingContact(Base):
	mapping_method = {
		'GET': 'get',
		'PUT': 'assign',
		'POST': 'modify',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_building):
		""" Return all contact for one building

		:param id_building: UUID
		"""
		with DB() as db:
			data = db.get_all("SELECT * FROM tbl_building_contact WHERE id_building=%s;", (id_building,))

		return {
			'data': data
		}

	def assign(self, args):
		""" Assign new contact to building

		:param args: {
			id_building: UUID,
			first_name: STRING,
			last_name: STRING,
			phone_number: INTEGER,
			phone_extension: INTEGER,
			pager_number: INTEGER,
			pager_code: STRING,
			cellular_number: INTEGER,
			other_number: INTEGER
		}
		"""
		with DB() as db:
			db.execute("""INSERT INTO tbl_building_contact (
							id_building_contact, id_building, first_name, last_name, phone_number, phone_extension, pager_number, pager_code,
							cellular_number, other_number, created_on, is_active
						  ) VALUES(uuid_generate_v4(), %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), True);""", (
				args['id_building'], args['first_name'], args['last_name'], args['phone_number'], args['phone_extension'],
				args['pager_number'], args['pager_code'], args['cellular_number'], args['other_number']
			))

		return {
			'message': 'building contact successfully assigned'
		}

	def modify(self, args):
		""" Modify all information for building contact

		:param args: {
			id_building_contact: UUID,
			first_name: STRING,
			last_name: STRING,
			phone_number: INTEGER,
			phone_extension: INTEGER,
			pager_number: INTEGER,
			pager_code: STRING,
			cellular_number: INTEGER,
			other_number: INTEGER,
		}
		"""
		with DB() as db:
			db.execute("""UPDATE tbl_building_contact SET
							first_name=%s, last_name=%s, phone_number=%s, phone_extension=%s, pager_number=%s, pager_code=%s,
							cellular_number=%s, other_number=%s
						  WHERE id_building_contact=%s;""", (
				args['first_name'], args['last_name'], args['phone_number'], args['phone_extension'], args['pager_number'],
				args['pager_code'], args['cellular_number'], args['other_number'], args['id_building_contact']
			))

		return {
			'message': 'building contact successfully modified'
		}

	def remove(self, id_building_contact):
		""" Remove building contact

		:param id_building_contact: UUID
		"""
		with DB() as db:
			db.execute("UPDATE tbl_building_contact SET is_active=%s WHERE id_building_contact=%;", (
				False, id_building_contact
			))

		return {
			'message': 'building contact successfully removed'
		}