import json
import uuid
from causeweb.storage.db import DB
from causeweb.site.multilang import MultiLang
from causeweb.apis.base import Base
from .surveyquestion import SurveyQuestion


class Survey(Base):
	table_name = 'tbl_survey'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_survey=None):
		""" Return the survey information

		:param id_survey: UUID
		"""
		if self.has_permission('RightTPI') is False:
			return self.no_access()

		with DB() as db:
			if id_survey is None:
				data = db.get_all("SELECT * FROM tbl_survey;")
			else:
				data = db.get_all("SELECT * FROM tbl_survey WHERE id_survey=%s;", (id_survey,))

		for key, row in enumerate(data):
			data[key]['name'] = MultiLang.get(row['id_language_content_name'])
			data[key]['questions'] = SurveyQuestion().get(row['id_survey'], True)['data']

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

		with DB() as db:
			db.execute("INSERT INTO tbl_survey(id_survey, id_language_content_name, survey_type, created_on, is_active) VALUES(%s, %s, %s, NOW(), True);", (
				id_survey, id_language_content, args['survey_type']
			))

		if 'questions' in args:
			self.set_questions(id_survey, args['questions'], True)

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

		with DB() as db:
			id_survey_answer = db.get("SELECT id_inspection FROM tbl_inspection WHERE id_survey=%s;", (args['id_survey'],))

			if id_survey_answer != '':
				self.remove(args['id_survey'])
				self.create(args)
			else:
				id_language_content = MultiLang.set(args['name'])

				db.execute("UPDATE tbl_survey SET id_language_content_name=%s, survey_type=%s, is_active=%s WHERE id_survey=%s;", (
					id_language_content, args['survey_type'], args['is_active'], args['id_survey']
				))

				if 'questions' in args:
					self.set_questions(args['id_survey'], args['questions'])

		return {
			'message': 'survey successfully modify'
		}

	def remove(self, id_survey):
		""" Remove a survey

		:param id_survey: UUID
		"""
		if self.has_permission('RightTPI') is False:
			return self.no_access()

		with DB() as db:
			db.execute("UPDATE tbl_survey SET is_active=%s WHERE id_survey=%s;", (
				False, id_survey
			))

		return {
			'message': 'survey successfully removed'
		}

	def set_questions(self, id_survey, questions, force_creation=False):
		if not isinstance(questions, dict) and not isinstance(questions, list):
			questions = json.loads(questions)

		for question in questions:
			question.update({
				'id_survey': id_survey
			})

			if 'id_survey_question' not in question or force_creation is True:
				SurveyQuestion().create(question)
			else:
				SurveyQuestion().modify(question)