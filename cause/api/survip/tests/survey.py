import unittest
from cause.api.management.core.database import Database
from ..resturls.survey import Survey
from ..resturls.surveychoice import SurveyChoice
from ..resturls.surveyquestion import SurveyQuestion


class TestSurvey(unittest.TestCase):
	def setUp(self):
		self.id_survey = None
		self.id_survey_choice = None
		self.id_survey_question = None

	def test_01_insert(self):
		result = Survey().create({
			'name': 'survey for unittest',
			'survey_type': 'residential'
		})

		self.__class__.id_survey = result['id_survey']
		self.assertEqual(result['message'], "survey successfully created")

	def test_02_get(self):
		result = Survey().get(self.__class__.id_survey)
		self.assertEqual(result['data'].name['fr'], 'survey for unittest')

	def test_03_modify(self):
		result = Survey().modify({
			'id_survey': self.__class__.id_survey,
			'name': 'survey for unittest+modify'
		})

		self.assertEqual(result['message'], "survey successfully modified")

	def test_04_get(self):
		result = Survey().get(self.__class__.id_survey)
		self.assertEqual(result['data'].name['fr'], 'survey for unittest+modify')

	def test_05_question_insert(self):
		result = SurveyQuestion().create({
			'title': 'survey question for unittest',
			'description': 'survey question description for unittest',
			'id_survey': self.__class__.id_survey
		})

		self.__class__.id_survey_question = result['id_survey_question']
		self.assertEqual(result['message'], "survey question successfully created")

	def test_06_question_get(self):
		result = SurveyQuestion().get(self.__class__.id_survey)
		self.assertEqual(result['data'][0].title['fr'], 'survey question for unittest')

	def test_07_question_modify(self):
		result = SurveyQuestion().modify({
			'id_survey_question': self.__class__.id_survey_question,
			'title': 'survey question for unittest+modify'
		})

		self.assertEqual(result['message'], "survey question successfully modified")

	def test_08_question_get(self):
		result = SurveyQuestion().get(self.__class__.id_survey)
		self.assertEqual(result['data'][0].title['fr'], 'survey question for unittest+modify')

	def test_09_choice_insert(self):
		result = SurveyChoice().create({
			'name': 'survey choice for unittest',
			'id_survey_question': self.__class__.id_survey_question
		})

		self.__class__.id_survey_choice = result['id_survey_choice']
		self.assertEqual(result['message'], "survey choice successfully created")

	def test_10_choice_get(self):
		result = SurveyChoice().get(self.__class__.id_survey_question)
		self.assertEqual(result['data'][0].name['fr'], 'survey choice for unittest')

	def test_11_choice_modify(self):
		result = SurveyChoice().modify({
			'id_survey_choice': self.__class__.id_survey_choice,
			'name': 'survey choice for unittest+modify'
		})

		self.assertEqual(result['message'], "survey choice successfully modified")

	def test_12_choice_get(self):
		result = SurveyChoice().get(self.__class__.id_survey_question)
		self.assertEqual(result['data'][0].name['fr'], 'survey choice for unittest+modify')

	def test_13_choice_remove(self):
		result = SurveyChoice().remove(self.__class__.id_survey_choice)
		self.assertEqual(result['message'], "survey choice successfully removed")

	def test_14_question_remove(self):
		result = SurveyQuestion().remove(self.__class__.id_survey_question)
		self.assertEqual(result['message'], "survey question successfully removed")

	def test_15_remove(self):
		result = Survey().remove(self.__class__.id_survey)
		self.assertEqual(result['message'], "survey successfully removed")

	def test_16_choice_delete(self):
		with Database() as db:
			db.execute("DELETE FROM tbl_survey_choice WHERE id_survey_choice::UUID='%s';" % self.__class__.id_survey_choice)

	def test_17_choice_delete(self):
		with Database() as db:
			db.execute("DELETE FROM tbl_survey_question WHERE id_survey_question::UUID='%s';" % self.__class__.id_survey_question)

	def test_18_delete(self):
		with Database() as db:
			db.execute("DELETE FROM tbl_survey WHERE id_survey::UUID='%s';" % self.__class__.id_survey)