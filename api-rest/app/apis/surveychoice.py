import uuid
from causeweb.storage.db import DB
from causeweb.site.multilang import MultiLang
from causeweb.apis.base import Base


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
		"""
		if self.has_permission('RightTPI') is False:
			return self.no_access()

		with DB() as db:
			if is_active is None:
				data = db.get_all("""SELECT *
								FROM tbl_survey_choice
								WHERE id_survey_question=%s
								ORDER BY sequence;""", (id_survey_question,))
			else:
				data = db.get_all("""SELECT *
								FROM tbl_survey_choice
								WHERE id_survey_question=%s AND is_active=%s
								ORDER BY sequence;""", (id_survey_question, is_active))

		for key, row in enumerate(data):
			data[key]['description'] = MultiLang.get(row['id_language_content'])

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
		id_language_content = MultiLang.set(args['description'], True)
		sequence = int(args['sequence']) if 'sequence' in args else 0
		next_question = args['id_survey_question_next'] if 'id_survey_question_next' in args and args['id_survey_question_next'] != '' else None

		with DB() as db:
			db.execute("""INSERT INTO
							tbl_survey_choice(id_survey_choice, id_survey_question, sequence, id_language_content, id_survey_question_next, is_active)
							VALUES(%s, %s, %s, %s, %s, %s);""", (
				id_survey_choice, args['id_survey_question'], sequence, id_language_content, next_question, True
			))

		return {
			'message': 'survey successfully create choice'
		}

	def modify(self, args):
		if self.has_permission('RightTPI') is False:
			return self.no_access()

		id_language_content = MultiLang.set(args['description'])
		sequence = args['sequence'] if 'sequence' in args else 0
		next_question = args['id_survey_question_next'] if 'id_survey_question_next' in args else None

		with DB() as db:
			db.execute("UPDATE tbl_survey_choice SET sequence=%s, id_language_content=%s, id_survey_question_next=%s, is_active=%s WHERE id_survey_choice=%s;", (
				sequence, id_language_content, next_question, args['is_active'], args['id_survey_choice']
			))

		return {
			'message': 'survey successfully modify choice'
		}

	def remove(self, id_survey_choice):
		if self.has_permission('RightTPI') is False:
			return self.no_access()

		with DB() as db:
			db.execute("UPDATE tbl_survey_choice SET is_active=%s WHERE id_survey_choice=%s;", (
				False, id_survey_choice
			))

		return {
			'message': 'survey successfully remove choice'
		}