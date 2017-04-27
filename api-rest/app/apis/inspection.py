import uuid
from causeweb.storage.db import DB
from causeweb.session.general import Session
from causeweb.apis.base import Base
from causeweb.apis.webuser import Webuser
from .building import Building


class Inspection(Base):
	table_name = 'tbl_inspection'
	mapping_method = {
		'GET': 'get',
		'PUT': 'assign',
		'POST': 'complete',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_city=None):
		""" Return all inspection for the connected user

		:param id_city: UUID
		"""
		with DB() as db:
			if id_city is None and self.has_permission('RightTPI') is True:
				data = db.get_all("SELECT * FROM tbl_inspection WHERE is_active=%s AND is_completed=%s", (True, False))
			elif id_city is None:
				data = db.get_all("SELECT * FROM tbl_inspection WHERE id_webuser=%s AND is_active=%s AND is_completed=%s", (
					Session.get('userId'), True, False
				))
			elif self.has_permission('RightTPI') is True:
				data = db.get_all("""SELECT * FROM tbl_inspection i
	                                LEFT JOIN tbl_building b ON b.id_building = i.id_building
	                                LEFT JOIN tbl_street s ON s.id_street = b.id_street
	                                WHERE i.is_active=%s AND i.is_completed=%s AND s.id_city=%s;""", (
	                  True, False, id_city
                  ))
			else:
				data = db.get_all("""SELECT * FROM tbl_inspection i
	                                LEFT JOIN tbl_building b ON b.id_building = i.id_building
	                                LEFT JOIN tbl_street s ON s.id_street = b.id_street
	                                WHERE i.id_webuser=%s AND i.is_active=%s AND i.is_completed=%s AND s.id_city=%s;""", (
					Session.get('userId'), True, False, id_city
				))

		for key, row in enumerate(data):
			data[key]['building'] = Building().get(row['id_building'])
			data[key]['webuser'] = Webuser().get(row['id_webuser'])

		return {
			'data': data
		}

	def complete(self, args):
		""" Mark inspection as done

		:param args: {
			id_inspection: UUID
		}
		"""
		with DB() as db:
			db.execute("UPDATE tbl_inspection SET id_webuser=%s, is_completed=%s WHERE id_inspection=%s;", (
				Session.get('userId'), True, args['id_inspection']
			))

		return {
			'message': 'inspection successfully complete'
		}

	def assign(self, args):
		""" Assign building inspection to someone

		:param args: {
			id_building: UUID,
			id_webuser: UUID,
			id_survey: UUID
		}
		"""
		if self.has_permission('RightTPI') is False:
			return self.no_access()

		id_inspection = uuid.uuid4()
		with DB() as db:
			db.execute("""INSERT INTO tbl_inspection(id_inspection, id_survey, id_building, id_webuser, created_by, is_active)
  						VALUES (%s, %s, %s, %s, %s, %s);""", (
				id_inspection, args['id_survey'], args['id_building'], args['id_webuser'], Session.get('userId'), True
			))

		return {
			'id_inspection': id_inspection,
			'message': 'inspection successfully assigned'
		}

	def remove(self, id_inspection):
		""" Remove inspection

		:param id_inspection: UUID
		"""
		if self.has_permission('RightTPI') is False:
			return self.no_access()

		with DB() as db:
			db.execute("UPDATE tbl_inspection SET is_active=%s WHERE id_inspection=%s;", (
				False, id_inspection
			))

		return {
			'message': 'inspection successfully removed'
		}