import uuid
from framework.manage.database import Database
from framework.manage.multilang import MultiLang
from framework.resturls.base import Base
from ..models.survey import SurveyChoice as Table


class SurveyChoice(Base):
	table_name = 'tbl_survey_choice'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_survey_question=None, is_active=None):
		""" Return all choices for one question

		:param id_survey_question: UUID
		:param is_active: BOOLEAN
		"""
		if self.has_permission('RightTPI') is False:
			return self.no_access()

		with Database() as db:
			if is_active is None:
				data = db.query(Table).filter(Table.id_survey_question == id_survey_question).all()
			else:
				data = db.query(Table).filter(
					Table.id_survey_question == id_survey_question,
					Table.is_active == is_active,
				).all()

		return {
			'data': data
		}

	def create(self, args):
		""" Create a choice for a question on survey

		:param args: {
			id_survey_question: UUID,
			sequence: INTEGER,
			description: JSON,
			id_survey_question_next: UUID
		}
		"""
		if self.has_permission('RightTPI') is False:
			return self.no_access()

		id_survey_choice = uuid.uuid4()
		id_language_content = MultiLang.set(args['name'], True)
		sequence = int(args['sequence']) if 'sequence' in args else 0
		next_question = args['id_survey_question_next'] if 'id_survey_question_next' in args and args['id_survey_question_next'] != '' else None

		with Database() as db:
			db.insert(Table(id_survey_choice, id_language_content, next_question, sequence))
			db.commit()

		return {
			'id_survey_choice': id_survey_choice,
			'message': 'survey choice successfully created'
		}

	def modify(self, args):
		if self.has_permission('RightTPI') is False:
			return self.no_access()

		next_question = args['id_survey_question_next'] if 'id_survey_question_next' in args else None

		with Database() as db:
			data = db.query(Table).get(args['id_survey_choice'])
			data.id_survey_question_next = next_question

			if 'name' in args:
				data.id_language_content_name = MultiLang.set(args['name'])
			if 'sequence' in args:
				data.sequence = MultiLang.set(args['sequence'])
			if 'is_active' in args:
				data.is_active = MultiLang.set(args['is_active'])

			db.commit()

		return {
			'message': 'survey choice successfully modify'
		}

	def remove(self, id_survey_choice):
		if self.has_permission('RightTPI') is False:
			return self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_survey_choice)
			data.is_active = False
			db.commit()

		return {
			'message': 'survey choice successfully removed'
		}