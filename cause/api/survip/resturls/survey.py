import uuid

from api.management.core.database import Database
from api.management.core.multilang import MultiLang
from cause.api.management.resturls.base import Base
from ..models.inspection import Inspection
from ..models.survey import Survey as Table


class Survey(Base):
	table_name = 'tbl_survey'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_survey=None, is_active=None):
		""" Return the survey information

		:param id_survey: UUID
		"""
		if self.has_permission('RightTPI') is False:
			return self.no_access()

		with Database() as db:
			if id_survey is None and is_active is None:
				data = db.query(Table).all()
			elif id_survey is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_survey)

		return {
			'data': data
		}

	def create(self, args):
		""" Create a new survey

		:param args: {
			name: JSON,
			survey_type: ENUM('test'),
			questions: JSON
		}
		"""
		if self.has_permission('RightTPI') is False:
			return self.no_access()

		id_survey = uuid.uuid4()
		id_language_content = MultiLang.set(args['name'], True)

		with Database() as db:
			db.insert(Table(id_survey, id_language_content, args['survey_type']))
			db.commit()

		return {
			'id_survey': id_survey,
			'message': 'survey successfully created'
		}

	def modify(self, args):
		""" Modify a survey

		:param args: {
			id_survey: UUID,
			name: JSON,
			survey_type: ENUM('test'),
			is_active: BOOLEAN,
			questions: JSON
		}
		"""
		if self.has_permission('RightTPI') is False:
			return self.no_access()

		if 'id_survey' not in args:
			raise Exception("You need to pass a id_survey")

		with Database() as db:
			inspection = db.query(Inspection).filter(
				Inspection.id_survey == args['id_survey'],
				Inspection.is_completed == True,
			).all()

			if len(inspection) > 0:
				self.remove(args['id_survey'])
				self.create(args)
			else:
				data = db.query(Table).get(args['id_survey'])

				if 'name' in args:
					data.id_language_content_name = MultiLang.set(args['name'])

				if 'survey_type' in args:
					data.survey_type = args['survey_type']
				if 'is_active' in args:
					data.is_active = args['is_active']

				db.commit()

		return {
			'message': 'survey successfully modified'
		}

	def remove(self, id_survey):
		""" Remove a survey

		:param id_survey: UUID
		"""
		if self.has_permission('RightTPI') is False:
			return self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_survey)
			data.is_active = False
			db.commit()

		return {
			'message': 'survey successfully removed'
		}
