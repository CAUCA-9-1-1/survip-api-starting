import json
import uuid
from causeweb.storage.db import DB
from causeweb.site.multilang import MultiLang
from causeweb.apis.base import Base
from .surveychoice import SurveyChoice


class SurveyQuestion(Base):
	table_name = 'tbl_survey_question'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_survey=None, is_active=None):
		""" Return all question for one survey

		:param id_survey: UUID
		"""
		if self.has_permission('RightTPI') is False:
			return self.no_access()

		with DB() as db:
			if is_active is None:
				data = db.get_all("""SELECT *
								FROM tbl_survey_question
								WHERE id_survey=%s
								ORDER BY sequence;""", (id_survey,))
			else:
				data = db.get_all("""SELECT *
								FROM tbl_survey_question
								WHERE id_survey=%s AND is_active=%s
								ORDER BY sequence;""", (id_survey, is_active))

		for key, row in enumerate(data):
			data[key]['title'] = MultiLang.get(row['id_language_content_title'])
			data[key]['description'] = MultiLang.get(row['id_language_content_description'])

			if row['question_type'] == 'choice':
				data[key]['choices'] = SurveyChoice().get(row['id_survey_question'], is_active)['data']

		return {
			'data': data
		}

	def create(self, args):
		""" Create a question for a survey

		:param args: {
			id_survey: UUID,
			title: JSON,
			description: JSON,
			sequence: INTEGER,
			id_survey_question_next: UUID
		}
		"""
		if self.has_permission('RightTPI') is False:
			return self.no_access()

		if 'title' not in args or 'description' not in args or 'id_survey' not in args:
			return {
				'message': 'not all parameter are pass to create a new question'
			}

		id_survey_question = uuid.uuid4()
		id_language_content_title = MultiLang.set(args['title'], True)
		id_language_content_description = MultiLang.set(args['description'], True)
		next_question = args['id_survey_question_next'] if 'id_survey_question_next' in args and args['id_survey_question_next'] != '' else None
		sequence = int(args['sequence']) if 'sequence' in args else 0
		question_type = args['question_type'] if 'question_type' in args else 'text'

		with DB() as db:
			db.execute("UPDATE tbl_survey_question SET sequence=(sequence + 1) WHERE sequence >= %s", (args['sequence'],))
			db.execute("""INSERT INTO tbl_survey_question
			           (id_survey_question, id_survey, id_language_content_title, id_language_content_description, id_survey_question_next, sequence, question_type, is_active)
			           VALUES(%s, %s, %s, %s, %s, %s, %s, %s);""", (
				id_survey_question, args['id_survey'], id_language_content_title, id_language_content_description, next_question, sequence, question_type, True
			))

		if 'choices' in args:
			self.set_choices(id_survey_question, args['choices'], True)

		return {
			'id_survey_question': id_survey_question,
			'message': 'survey successfully create question'
		}

	def modify(self, args):
		if self.has_permission('RightTPI') is False:
			return self.no_access()

		if 'step' in args:
			return self.change_sequence(args)

		id_language_content_title = MultiLang.set(args['title'])
		id_language_content_description = MultiLang.set(args['description'])
		next_question = args['id_survey_question_next'] if 'id_survey_question_next' in args and args['id_survey_question_next'] != '' else None

		with DB() as db:
			db.execute("""UPDATE tbl_survey_question
					SET id_language_content_title=%s, id_language_content_description=%s, id_survey_question_next=%s, sequence=%s, question_type=%s, is_active=%s
					WHERE id_survey_question=%s;""", (
				id_language_content_title, id_language_content_description, next_question, args['sequence'], args['question_type'], True, args['id_survey_question']
			))

		if 'choices' in args:
			self.set_choices(args['id_survey_question'], args['choices'])

		return {
			'message': 'survey successfully modify question'
		}

	def remove(self, id_survey_question):
		if self.has_permission('RightTPI') is False:
			return self.no_access()

		with DB() as db:
			db.execute("UPDATE tbl_survey_question SET is_active=%s WHERE id_survey_question=%s;", (
				False, id_survey_question
			))

		return {
			'message': 'survey successfully remove question'
		}

	def change_sequence(self, args):
		with DB() as db:
			sequence = db.get("SELECT sequence FROM tbl_survey_question WHERE id_survey_question=%s;", (args['id_survey_question'],))
			new_sequence = int(sequence) + int(args['step'])

			db.execute("UPDATE tbl_survey_question SET sequence=(sequence + %s) WHERE sequence=%s;", ((int(args['step']) * -1), new_sequence))
			db.execute("UPDATE tbl_survey_question SET sequence=%s WHERE id_survey_question=%s;", (new_sequence, args['id_survey_question']))

		return {
			'message': 'survey successfully change sequence question'
		}

	def set_choices(self, id_survey_question, choices, force_creation=False):
		if not isinstance(choices, dict) and not isinstance(choices, list):
			choices = json.loads(choices)

		for choice in choices:
			choice.update({
				'id_survey_question': id_survey_question
			})

			if 'id_survey_choice' not in choice or force_creation is True:
				SurveyChoice().create(choice)
			else:
				SurveyChoice().modify(choice)