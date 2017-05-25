import json
import uuid
from .database import Database
from .utilities import Utilities
from ..models.language_content import LanguageContent

class MultiLang:
	@staticmethod
	def get(id_language_content):
		json_data = {'id_language_content': ''}

		try:
			with Database() as db:
				data = db.query(LanguageContent).get(id_language_content)

			json_data = {'id_language_content': id_language_content}
			json_data.update(Utilities.list_to_dict(data, 'language_code', 'description'))
		except:
			pass

		return json_data

	@staticmethod
	def set(description, force_create=False):
		if not isinstance(description, dict):
			try:
				description = json.loads(description)
			except:
				description = {'fr': description}

		id_language_content = description['id_language_content'] if 'id_language_content' in description else None

		if id_language_content is None or id_language_content == '' or force_create is True:
			id_language_content = uuid.uuid4()
			MultiLang.create(id_language_content, description)
		else:
			MultiLang.modify(id_language_content, description)

		return id_language_content

	@staticmethod
	def create(id_language_content, description):
		with Database() as db:
			for language_code in description:
				if language_code != 'id_language_content':
					db.add(LanguageContent(id_language_content, language_code, description[language_code]))
					db.commit()

	@staticmethod
	def modify(id_language_content, description):
		with Database() as db:
			for language_code in description:
				if language_code != 'id_language_content':
					data = db.query(LanguageContent).filter(
						LanguageContent.id_language_content == id_language_content,
						LanguageContent.language_code == language_code
					).first()

					data.description = description[language_code]
					db.commit()