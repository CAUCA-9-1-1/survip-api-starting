from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from framework.manage.multilang import MultiLang
from framework.models.language_content import LanguageContent


Base = declarative_base()


class Survey(Base):
	__tablename__ = "tbl_survey"

	id_survey = Column(String(36), primary_key=True)
	id_language_content_name = Column(String(36), ForeignKey(LanguageContent.id_language_content), nullable=False)
	survey_type = Column(String(36))
	created_on = Column(DateTime, default=datetime.now)
	is_active = Column(Boolean, default=True)

	@hybrid_property
	def name(self):
		return MultiLang.get(self.id_language_content_name)

	def __init__(self, id_survey, id_language_content, survey_type):
		self.id_survey = id_survey
		self.id_language_content_name = id_language_content
		self.survey_type = survey_type


class SurveyQuestion(Base):
	__tablename__ = "tbl_survey_question"

	id_survey_question = Column(String(36), primary_key=True)
	id_survey = Column(String(36), ForeignKey(Survey.id_survey), nullable=False)
	id_language_content_title = Column(String(36), ForeignKey(LanguageContent.id_language_content), nullable=False)
	id_language_content_description = Column(String(36), ForeignKey(LanguageContent.id_language_content), nullable=False)
	id_survey_question_next = Column(String(36))
	sequence = Column(Integer)
	question_type = Column(String(20))
	created_on = Column(DateTime, default=datetime.now)
	is_active = Column(Boolean, default=True)

	@hybrid_property
	def title(self):
		return MultiLang.get(self.id_language_content_title)

	@hybrid_property
	def description(self):
		return MultiLang.get(self.id_language_content_description)

	def __init__(self, id_survey_question, id_survey, id_language_content_title, id_language_content_description, id_survey_question_next, sequence):
		self.id_survey_choice = id_survey_question
		self.id_survey = id_survey
		self.id_language_content_title = id_language_content_title
		self.id_language_content_description = id_language_content_description
		self.id_survey_question_next = id_survey_question_next
		self.sequence = sequence


class SurveyChoice(Base):
	__tablename__ = "tbl_survey_choice"

	id_survey_choice = Column(String(36), primary_key=True)
	id_survey_question = Column(String(36), ForeignKey(SurveyQuestion.id_survey_question), nullable=False)
	id_language_content_name = Column(String(36), ForeignKey(LanguageContent.id_language_content), nullable=False)
	id_survey_question_next = Column(String(36))
	sequence = Column(Integer)
	created_on = Column(DateTime, default=datetime.now)
	is_active = Column(Boolean, default=True)

	@hybrid_property
	def name(self):
		return MultiLang.get(self.id_language_content_name)

	def __init__(self, id_survey_choice, id_survey_question, id_language_content, id_survey_question_next, sequence):
		self.id_survey_choice = id_survey_choice
		self.id_survey_question = id_survey_question
		self.id_language_content_name = id_language_content
		self.id_survey_question_next = id_survey_question_next
		self.sequence = sequence