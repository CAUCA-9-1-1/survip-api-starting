import uuid

from causepy.manage.database import Database
from causepy.urls.base import Base
from ..models.inspection import Inspection as Table


class Inspection(Base):
	table_name = 'tbl_inspection'
	mapping_method = {
		'GET': 'get',
		'PUT': 'assign',
		'POST': 'complete',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_inspection=None, is_active=None):
		""" Return all inspection information

		:param id_inspection: UUID
		:param is_active: Boolean
		"""
		with Database() as db:
			if id_inspection is None and is_active is None:
				data = db.query(Table).all()
			elif id_inspection is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_inspection)

		return {
			'data': data
		}

	def complete(self, args):
		""" Mark inspection as done

		:param args: {
			id_inspection: UUID
		}
		"""
		with Database() as db:
			data = db.query(Table).filter(Table.id_inspection == args['id_inspection']).first()
			data.is_completed = True
			db.commit()

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
		with Database() as db:
			db.insert(Table(id_inspection, args['id_survey'], args['id_building'], args['id_webuser']))
			db.commit()

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

		with Database() as db:
			data = db.query(Table).filter(Table.id_inspection == id_inspection).first()
			data.is_active = False
			db.commit()

		return {
			'message': 'inspection successfully removed'
		}